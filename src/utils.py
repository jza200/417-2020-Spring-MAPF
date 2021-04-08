import networkx as nx
from single_agent_planner import move, is_constrained, get_path

def construct_mdd(my_map, agent, start, goal, h_values, cost, constraints):
    '''
    This method build a single agent mdd
    '''
	mdd = nx.DiGraph()
	h_value = h_values[start_loc]
	explore = []
	# build contraint table for agent
	constraintTable = build_constraint_table(constraints, agent)

	root = {'loc': start_loc, 'g_val': 0, 'h_val': h_value, 'parent': None, 'timestep':0}
	explore.append(root)

	while len(explore) > 0:
		curr = explore.pop(0)
		if curr['timestep'] == cost:
			# Check cuur is goal or not
			if curr['loc'] == goal_loc:
				path = get_path(curr)
				for i in range(len(path) - 1):
					mdd.add_edge((path[i], i), (path[i+1], i+1))
			continue

		# Expand the current node
		for dir in range(5):
			child_loc = move(curr['loc'], dir)
			# Check whether the child location is outside the map
			if child_loc[0] < 0 or child_loc[0] >= len(my_map) \
			or child_loc[1] < 0 or child_loc[1] >= len(my_map[0]):
				continue
			# Check whether the child location is an obstacle 
			if my_map[child_loc[0]][child_loc[1]]:
				continue
			# Check whether the child location violates any constraints
			if is_constrained(curr['loc'], child_loc, curr['timestep'] + 1, constraintTable):
				continue
			# Check whether the g_val + h_value is larger than cost
			if curr['g_val'] + h_values[child_loc] + 1 > cost:
				continue

			child = {'loc': child_loc,
					'g_val': curr['g_val'] + 1,
					'h_val': h_values[child_loc],
					'parent': curr,
					'timestep': curr['timestep'] + 1}
			explore.append(child)
	return mdd

def merge_mdd(mdd1, mdd2, start1, start2, goal1, goal2):
    '''
    This method merges two mdds  

    Input:
    mdd1    - an mdd for one of the agents 
    mdd2    - an mdd for another agent
    start1  - start for one of the agents 
    start2  - start for another agent
    goal1   - goal for one of the agents 
    goal2   - goal for another agent

    Output: 
    joint_mdd
    joint_mdd_depth

    '''
    # If depths of mdd1 and mdd2 are not the same
    len1 = len(reconstruct_mdd(mdd1, start1))
    len2 = len(reconstruct_mdd(mdd2, start2))

    mdd1_new = mdd1.copy()
    mdd2_new = mdd2.copy()
    if len1 > len2:
        edges = []
        for i in range(len2, len1):
            edges.append(((goal2, i-1), (goal2, i)))
        mdd2_new.add_edges_from(edges)
    elif len1 < len2:
        edges = []
        for i in range(len1, len2):
            edges.append(((goal1, i-1), (goal1, i)))
        mdd1_new.add_edges_from(edges)

    # Megre two mdds
    joint_mdd = {0:[(start1, start2)]}
    for i in range(max(len1, len2) - 1):
        joint_mdd[i+1] = []
        for pair in joint_mdd[i]:
            successor1 = [successor for successor, _ in list(mdd1_new.successors((pair[0], i)))]
            successor2 = [successor for successor, _ in list(mdd2_new.successors((pair[1], i)))]
            cross_product = [(x, y) for x in successor1 for y in successor2 if x != y]

            for new_pair in cross_product:
                if new_pair not in joint_mdd[i+1]:
                    joint_mdd[i+1].append(new_pair)

        if len(joint_mdd[i+1]) == 0:
            return joint_mdd, max(len1, len2)-1
    joint_mdd_depth = max(len1, len2)-1
            
    return joint_mdd, joint_mdd_depth

def reconstruct_mdd(mdd, start):
    '''
    This method reconstruct mdd according to timestep
    '''
    new_mdd = {}
    # Append locations to their corresponding timesteps
    locations = nx.single_source_shortest_path_length(mdd, (start, 0)) 
    for loc, depth in locations.items():
        if depth not in new_mdd:
            new_mdd[depth] = []
        new_mdd[depth].append(loc[0])
    return new_mdd

def update_mdd(mdd, agent, start, goal, cost, constraints):
    '''
    This method update mdd according to timestep
    '''
    constraintTable = build_constraint_table(constraints, agent)
    mdd_new = mdd.copy()
    mdd_reconstructed = reconstruct_mdd(mdd, start)

    for timestep, locations in mdd_reconstructed.items():	
        # If the current location is goal location
        # then stop search
        if locations[0] == goal:	
            break
        else: 
            for curr_loc in locations:
                for next_loc in list(mdd_new.successors((curr_loc, timestep))):
                    if is_constrained(curr_loc, next_loc[0], timestep+1, constraintTable):
                        mdd_new.remove_edge((curr_loc, timestep), next_loc)
    # Remove nodes in the directed graph that do not have successors or predecessors
    deleted_nodes = []
    for node in nx.nodes(mdd_new):
        if node == (start_loc, 0):
            continue
        elif node != (goal, cost):
            if len(list(mdd_new.predecessors(node))) == 0 or len(list(mdd_new.successors(node))) == 0:
                deleted_nodes.append(node)
    mdd_new.remove_nodes_from(deleted_nodes)		
    return mdd_new

def build_constraint_table(constraints, agent):
    '''
    This method build constraint table for agent
    '''
    table = {}
    for constraint in constraints:
        if constraint['agent'] == agent:
            timestep = constraint['timestep']
            if ts not in table:
                table[constraint['timestep']] = []
            table[timestep].append(constraint)
        elif constraint['agent'] == 'goal':
            if 'goal' not in table:
                table['goal'] = []
            table['goal'].append(constraint)
        elif constraint['positive'] is True:
            constraint['agent'] = agent
            constraint['positive'] = False
            constraint['loc'].reverse()
            timestep = constraint['timestep']
            if timestep not in table:
                table[constraint['timestep']] = []
            table[timestep].append(constraint)
    return table
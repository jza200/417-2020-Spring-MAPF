import networkx as nx

def construct_mdd(cost_minimal_paths):
    """ 
    this method returns an mdd graph given all the cost minimal paths

    cost_minimal_paths - an array containing all cost minimal paths 
        e.g. [[(2,1), (3,1), (3,2)],[(2,1), (2,2), (3,3)]]
    """
    if len(cost_minimal_paths) == 0:
        raise BaseException("empty list :- cost-minimal paths.")

    for i in range(len(cost_minimal_paths)):
        if len(cost_minimal_paths[0]) != len(cost_minimal_paths[i]):
            raise BaseException("size cost minimal paths different for one of the cost-minimal paths")

        if cost_minimal_paths[0][0] != cost_minimal_paths[i][0]:
            raise BaseException("start locations different for one of the cost-minimal paths.")
    
    mdd = dict() # acyclic graph 

    for path in cost_minimal_paths:
        path_len = len(path)
        for i in range(path_len):
            curr_loc = path[i]
            if(i < path_len-1):
                next_loc = path[i+1]
                # check if curr loc in mdd 
                if curr_loc not in mdd:
                    mdd[curr_loc] = [next_loc] # create new node
                else: 
                    mdd[curr_loc] = list(set(mdd[curr_loc] + [next_loc])) # add children nodes
            else:
                # add terminal 
                mdd[curr_loc] = None
    return mdd 

def detect_dependency(mdd1, mdd2):
    """
    This method makes a joint mdd from mdd1 and mdd2 and returns false if the joint 
    mdd does not contain goal node; returns true otherwise.

    mdd1 - an mdd for one of the agents 
    mdd2 - an mdd for another agent 
    """

    # add dummy terminal veritces

    # construct mdd

    # check if mdd contains goal node

    pass

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
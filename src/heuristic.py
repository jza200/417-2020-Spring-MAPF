import networkx as nx
from utils import merge_mdd, reconstruct_mdd
from cbs import CBSSolver

def compute_CG(mdds, num_of_agents, starts): 
    '''
    compute_CG is to compute CG heuristic

    '''
    # Construct conflict graph according to cardinal conflict
    conflict_graph = construct_conflict_graph(num_of_agents, mdds)
    # Compute heuristic
    h_value = mvc(conflict_graph)

    return h_value

def construct_conflict_graph(num_of_agents, mdds):
    '''
    num_of_agents      - number of agents 
    mdds            - all agents mdd. structure: mdds[number of agents]
    '''
    conflict_graph = nx.Graph()

    for outer_agent in range(num_of_agents):
        for inner_agent in range(outer_agent + 1, num_of_agents):
            a1_mdd = mdds[outer_agent]
            a2_mdd = mdds[inner_agent]

            min_path_length = min(len(a2_mdd.keys()), len(a1_mdd.keys()))

            for timestep in range(min_path_length):
                if len(a1_mdd[timestep]) == 1 and len(a2_mdd[timestep]) == 1:
                    if a1_mdd[timestep][0] == a2_mdd[timestep][0]:
                        conflict_graph.add_edge(inner_agent, outer_agent)

    return conflict_graph

def compute_DG(mdds, num_of_agents, starts, goals):
    '''
    this method computes DG heuristic

    '''
    # Construct dependency graph
    dependency_graph = construct_dependency_graph(num_of_agents, mdds, starts, goals)
    # Compute heuristic
    h_value = get_MVC(dependency_graph)

    return h_value

def construct_dependency_graph(num_of_agents, mdds, starts, goals):
    '''
    This method computes dependency graph(DG)

    '''
    dependency_graph = nx.Graph()
    # Check whether agent i and agent j have cardinal conflicts
    for i in range(num_of_agents - 1):
        for j in range(i + 1, num_of_agents):
            # Merge two mdds
            joint_mdd, max_depth = merge_mdd(mdds[i], mdds[j], starts[i], starts[j], goals[i], goals[j])
            # If two agent are dependent
            if isDependent(joint_mdd, goals[i], goals[j], max_level) or hasCardinal(mdds[i], mdds[j], starts[i], starts[j]):
                dependency_graph.add_nodes_from([i, j])
                dependency_graph.add_edge(i, j)
    return dependency_graph

def compute_WDG(my_map, num_of_agents, mdds, paths, constraints, starts, goals):
    '''
    this method computes WDG heuristic

    '''
    # Construct dependency graph
    dependency_graph = construct_dependency_graph(num_of_agents, mdds, starts, goals)
    # Compute weighted dependency graph
    weight_dependency_graph = compute_weight_dependency_graph(my_map, paths, constraints, num_of_agents, dependency_graph, starts, goals)
    # Compute heuristic
    h_value = compute_EWMVC(weight_dependency_graph)
    return h_value

def compute_weight_dependency_graph(my_map, dependency_graph, paths, constraints, num_of_agents, starts, goals):
    '''
    This method computes weight dependency graph(WDG)

    '''
    g = dependency_graph.copy()
    for i in range(num_of_agents - 1):
        for j in range(i, num_of_agents):
            if (i, j) in g.edges:
                # If agent i and agent j have conflict, use CBS to get the cost of conflict-free paths between two agents
                constraints_ij = [constraint.copy() for constraint in constraints if constraint['agent'] == i or constraint['agent'] == j]
                for constraint in constraints_ij:
                    if constraint['agent'] == i:
                        constraint['agent'] = 0
                    elif constraint['agent'] == j:
                        constraint['agent'] = 1
                starts_2 = [starts[i], starts[j]]
                goals_2 = [goals[i], goals[j]]
                cbs = CBSSolver(my_map, starts_2, goals_2)
                cost, root_paths, root_constraints = cbs.find_solution(disjoint = False, heuristic = 'None', weight = True, constraints = constraints_ij) 
                weight = cost - len(paths[i]) - len(paths[j]) + 2
                g.add_edge(i, j, weight = weight)
    return g

def compute_EWMVC(weight_dependency_graph):
    '''
    This method compute h_value for WDG
    '''
    # Wait for team member
    pass

def isDependent(joint_mdd, goal1, goal2, max_depth):
    '''
    The method check if two agents are dependent
    '''
    # If joint_mdd has arrived at the max_depth
    if max_depth in joint_mdd and (goal1, goal2) in joint_mdd[max_depth]:
        return False
    return True

def hasCardinal(mdd1, mdd2, start1, start2):
    # Reconstruct mdd according to timestep
    mdd1 = reconstruct_mdd(mdd1, start1)
    mdd2 = reconstruct_mdd(mdd2, start2)

    cost = min(len(MDD1), len(mdd2))
    for timestep in range(cost):
        if len(mdd1[timestep]) == 1 and len(mdd2[timestep]) == 1 and mdd1[timestep][0] == mdd2[timestep][0]:
            # Cardinal vertex
            return True
        if timestep < cost - 1:
            # Cardinal Edge
            if len(mdd1[timestep]) == 1 and len(mdd2[timestep]) == 1 and len(mdd1[timestep+1]) == 1 and len(mdd2[timestep+1]) == 1 \
            and mdd1[timestep][0] == mdd2[timestep+1][0] and mdd1[timestep+1][0] == mdd2[timestep][0]:
                return True
    return False

def mvc(graph):
    '''
    Get mvc for graph

    '''
    for k in range(1, graph.number_of_nodes()):
        if k_vertex_cover(graph, k):
            return k

def k_vertex_cover(graph, k):
    '''
    Check whether a graph has a vertext cover of k or not 

    '''
    if g.number_of_edges() == 0:
        return True
    elif g.number_of_edges() > k*g.number_of_nodes():
        return False

    v = list(graph.edges())[0]
    graph1 = graph.copy()
    graph2 = graph.copy()

    graph1.remove_node(v[0])
    graph2.remove_node(v[1])

    return k_vertex_cover(graph1, k-1) or k_vertex_cover(graph2, k-1)
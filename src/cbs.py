import time as timer
import heapq
import random
import networkx as nx
from single_agent_planner import compute_heuristics, a_star, get_location, get_sum_of_cost
from heuristic import compute_CG, compute_DG, compute_WCG
from utils import update_mdd


def detect_collision(path1, path2):
    ##############################
    # Task 3.1: Return the first collision that occurs between two robot paths (or None if there is no collision)
    #           There are two types of collisions: vertex collision and edge collision.
    #           A vertex collision occurs if both robots occupy the same location at the same timestep
    #           An edge collision occurs if the robots swap their location at the same timestep.
    #           You should use "get_location(path, t)" to get the location of a robot at time t.

    max_timestep = max(len(path1),len(path2))

    collision = dict()

    for t in range (0, max_timestep):
        # Vertex collision
        if get_location(path1,t) == get_location(path2,t):
            collision = {
                'loc': [get_location(path1,t)], 
                'timestep' : t
                }

        # Edge collision
        if t != 0 and get_location(path1,t-1) == get_location(path2,t) and get_location(path1,t) == get_location(path2,t-1):
            collision = {
                'loc': [get_location(path2,t-1),get_location(path2,t)],
                 'timestep': t
                 }
        

    return collision


def detect_collisions(paths):
    ##############################
    # Task 3.1: Return a list of first collisions between all robot pairs.
    #           A collision can be represented as dictionary that contains the id of the two robots, the vertex or edge
    #           causing the collision, and the timestep at which the collision occurred.
    #           You should use your detect_collision function to find a collision between two robots.

    agents = len(paths)
    print(agents)
    collisions = list()

    for a1 in range(0,agents-1):
        for a2 in range (a1+1,agents):
            collision_loc = detect_collision(paths[a1],paths[a2])
            if collision_loc:
                collisions.append({
                    'a1': a1, 
                    'a2': a2,
                    'loc': collision_loc['loc'], 
                    'timestep': collision_loc['timestep']
                    }
                )

    return collisions


def standard_splitting(collision):
    ##############################
    # Task 3.2: Return a list of (two) constraints to resolve the given collision
    #           Vertex collision: the first constraint prevents the first agent to be at the specified location at the
    #                            specified timestep, and the second constraint prevents the second agent to be at the
    #                            specified location at the specified timestep.
    #           Edge collision: the first constraint prevents the first agent to traverse the specified edge at the
    #                          specified timestep, and the second constraint prevents the second agent to traverse the
    #                          specified edge at the specified timestep

    loc = collision['loc']
    timestep = collision['timestep']

    if len(loc) == 1:
        first_constraint = {
            'agent': collision['a1'], 
            'loc': [loc[0]], 
            'timestep': timestep
        }

        second_constraint = {
            'agent': 
            collision['a2'], 
            'loc': [loc[0]], 
            'timestep': timestep
        }

        return [first_constraint, second_constraint]
    
    if len(loc) > 1:
        first_constraint = {
            'agent': collision['a1'], 
            'loc': [loc[1],loc[0]], 
            'timestep': timestep
            }

        second_constraint = {
            'agent': collision['a2'], 
            'loc': [loc[0],loc[1]], 
            'timestep': timestep
            }
            
        return [first_constraint,second_constraint]


def disjoint_splitting(collision):
    ##############################
    # Task 4.1: Return a list of (two) constraints to resolve the given collision
    #           Vertex collision: the first constraint enforces one agent to be at the specified location at the
    #                            specified timestep, and the second constraint prevents the same agent to be at the
    #                            same location at the timestep.
    #           Edge collision: the first constraint enforces one agent to traverse the specified edge at the
    #                          specified timestep, and the second constraint prevents the same agent to traverse the
    #                          specified edge at the specified timestep
    #           Choose the agent randomly

    loc = collision['loc']
    timestep = collision['timestep']


    if random.randint(0,1):
        random_agent = 'a1'
    else:
        random_agent = 'a2'

    if len(loc)>1 and random_agent == 'a1':

        first_constraint = {
            'agent': collision['a1'], 
            'loc': [loc[1],loc[0]], 
            'timestep': timestep, 
            'positive': True
            }

        second_constraint = {
            'agent': collision['a1'], 
            'loc': [loc[1],loc[0]], 
            'timestep': timestep, 
            'positive': False
            }
        
        return [first_constraint,second_constraint]

    if len(loc)>1 and random_agent == 'a2':
        first_constraint = {
            'agent' : collision['a2'], 
            'loc' : [loc[0],loc[1]], 
            'timestep' : timestep, 
            'positive' : True
            }

        second_constraint = {
            'agent' : collision['a2'], 
            'loc' : [loc[0],loc[1]], 
            'timestep' : timestep, 
            'positive' : False
            }
        
        return [first_constraint,second_constraint]

    if len(loc) == 1:
        first_constraint = {
            'agent' : collision[random_agent], 
            'loc' : [loc[0]], 
            'timestep' : timestep,
             'positive' : True
            }
        second_constraint = {
            'agent' : collision[random_agent], 
            'loc' : [loc[0]], 
            'timestep' : timestep,
             'positive' : False
             }
        
        return [first_constraint,second_constraint]

def paths_violate_constraint(constraint, paths):
    assert constraint['positive'] is True
    rst = []
    for i in range(len(paths)):
        if i == constraint['agent']:
            continue
        curr = get_location(paths[i], constraint['timestep'])
        prev = get_location(paths[i], constraint['timestep'] - 1)
        if len(constraint['loc']) == 1:  # vertex constraint
            if constraint['loc'][0] == curr:
                rst.append(i)
        else:  # edge constraint
            if constraint['loc'][0] == prev or constraint['loc'][1] == curr \
                    or constraint['loc'] == [curr, prev]:
                rst.append(i)
    return rst

def construct_mdds(my_map, num_of_agents,starts, goals, h_values, paths, constraints):
    pass

class CBSSolver(object):
    """The high-level search of CBS."""

    def __init__(self, my_map, starts, goals):
        """my_map   - list of lists specifying obstacle positions
        starts      - [(x1, y1), (x2, y2), ...] list of start locations
        goals       - [(x1, y1), (x2, y2), ...] list of goal locations
        """

        self.my_map = my_map
        self.starts = starts
        self.goals = goals
        self.num_of_agents = len(goals)

        self.num_of_generated = 0
        self.num_of_expanded = 0
        self.CPU_time = 0

        self.open_list = []

        self.construct_mdd = 0
        self.update_mdd = 0

        # compute heuristics for the low-level search
        self.heuristics = []
        for goal in self.goals:
            self.heuristics.append(compute_heuristics(my_map, goal))

    def push_node(self, node):
        heapq.heappush(self.open_list, (node['cost'], len(node['collisions']), self.num_of_generated, node))
        print("Generate node {}".format(self.num_of_generated))
        self.num_of_generated += 1

    def pop_node(self):
        _, _, id, node = heapq.heappop(self.open_list)
        print("Expand node {}".format(id))
        self.num_of_expanded += 1
        return node

    def find_solution(self, disjoint=True):
        """ Finds paths for all agents from their start locations to their goal locations

        disjoint    - use disjoint splitting or not
        """

        self.start_time = timer.time()

        # Generate the root node
        # constraints   - list of constraints
        # paths         - list of paths, one for each agent
        #               [[(x11, y11), (x12, y12), ...], [(x21, y21), (x22, y22), ...], ...]
        # collisions     - list of collisions in paths
        root = {'cost': 0,
                'constraints': [],
                'paths': [],
                'collisions': [],
                'mdd': []}
        root['constraints'] = constraints.copy()
        for i in range(self.num_of_agents):
            path = a_star(self.my_map, self.starts[i], self.goals[i], self.heuristics[i], i, root['constraints'])
            if path is None:
                raise BaseException('No solutions')
            root['paths'].append(path)

        root['cost'] = get_sum_of_cost(root['paths'])
        root['collisions'] = detect_collisions(root['paths'])

        # Build initial mdds
        if heuristic != 'None':
            start_construct = timer.time()
            mdds = construct_mdds()
            root['mdd'] = mdds
            self.push_node(root)
            self.construct_mdd += timer.time() - start_construct

            h_value = 0
            if heuristic == 'CG':
                # Compute CG heuristic
                h_value= compute_CG(mdds, self.num_of_agents, self.starts)
            elif heuristic == 'DG':
                # Compute DG heuristic
                h_value = compute_DG(mdds, self.num_of_agents, self.starts, self.goals)
            elif heuristic == 'WDG':
                # Compute WDG heuristic
                h_value = compute_WDG(self.my_map, mdds, root['paths'], root['constraints'], self.num_of_agents, self.starts, self.goals)
	
        # Save mdds for all agents
        mdd_all = []
        for i in range(self.num_of_agents):
            mdd_i = {}
            mdd_i[len(root['paths'][i])-1] = mdds[i].copy()
            mdd_all.append(mdd_i)

        # Task 3.3: High-Level Search
        #           Repeat the following as long as the open list is not empty:
        #             1. Get the next node from the open list (you can use self.pop_node()
        #             2. If this node has no collision, return solution
        #             3. Otherwise, choose the first collision and convert to a list of constraints (using your
        #                standard_splitting function). Add a new child node to your open list for each constraint
        #           Ensure to create a copy of any objects that your child nodes might inherit

        disjoint = True
        while len(self.open_list) > 0:
            N = self.pop_node()
            if len(N['collisions']) == 0:
                if weight:
                    cost = get_sum_of_cost(P['paths'])
                    return cost, N['paths'], root['constraints']
                self.print_results(P)
                return N['paths']
            collision = N['collisions'][0]
            if disjoint:
                constraints = disjoint_splitting(collision)
            else:
                constraints = standard_splitting(collision)
            for constraint in constraints:
                isAdd = True
                Q = {}
                Q['constraints'] = N['constraints'] + [constraint]
                Q['paths'] = [path.copy() for path in P['paths']]
                Q['mdd'] = [mdd.copy() for mdd in N['mdd']]

                if constraint['positive'] == False:
                    agent = constraint['agent']
                    path = a_star(self.my_map, self.starts[agent], self.goals[agent], self.heuristics[agent],
                            agent, Q['constraints']) 
                    if path is not None:
                        Q['paths'][agent] = path.copy()
                        if heuristic != 'None':
                            # Update mdd for agent
                            if len(N['paths'][agent]) < len(path):
                                mdd_temp = 0
                                # If the mdd with new depth is already in the depth
                                if (len(path) - 1) in mdd_all[agent]: 
                                    
                                    mdd_temp = mdd_all[agent][len(path)-1].copy()
                                else:
                                    start_construct = timer.time()
                                    # Wait for team member to complete
                                    #mdd_temp =  construct_mdd()
                                    self.construct_mdd += timer.time() - start_construct
                                    mdd_all[agent][len(path)-1] = mdd_temp.copy()
                                Q['mdd'][agent] = mdd_temp.copy()
                            
                            start_update = timer.time()
                            Q['mdd'][agent] = update_mdd(Q['mdd'][agent], agent, self.starts[agent], self.goals[agent], len(path) - 1, Q['constraints'])
                            self.update_mdd += timer.time() - start_update
                    else:
                        isAdd = False
                    
                if isAdd:
                    Q['collisions'] = detect_collisions(Q['paths'])
                    h_value = 0
                    if heuristic == 'CG':
                        # Compute CG heuristic
                        h_value = compute_CG(Q['mdd'], self.num_of_agents, self.starts)
                    elif heuristic == 'DG':
                        # Compute DG heuristic
                        h_value = compute_DG(Q['mdd'], self.num_of_agents, self.starts, self.goals)
                    elif heuristic == 'WDG':
                        # Compute WDG heuristic
                        h_value = compute_WDG(self.my_map, Q['mdd'], Q['paths'],Q['constraints'], self.num_of_agents, self.starts, self.goals)
                        
                    Q['cost'] = get_sum_of_cost(Q['paths']) + h_value
                    
                    self.push_node(Q)
		
        return root['paths']


    def print_results(self, node):
        print("\n Found a solution! \n")
        CPU_time = timer.time() - self.start_time
        print("CPU time (s):    {:.2f}".format(CPU_time))
        print("Heuristic:    {}".format(self.heuristic))
        print("Construct MDD time (s):    {:.2f}".format(self.construct_mdd))
        print("Update MDD time (s):    {:.2f}".format(self.update_mdd))
        print("Sum of costs:    {}".format(get_sum_of_cost(node['paths'])))
        print("Expanded nodes:  {}".format(self.num_of_expanded))
        print("Generated nodes: {}".format(self.num_of_generated))

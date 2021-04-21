'''
This script is used for generate random testing cases
''' 
import random
import math
from collections import deque
from pathlib import Path

NUM_WALKS = pow(2, 16) 
MAP_SIZES = [14, 62]
NUM_TRIALS = 30
NUM_AGENTS = [2, 8, 16]


def move(loc, dir):
    directions = [(0, -1), (1, 0), (0, 1), (-1, 0), (0, 0)]
    return loc[0] + directions[dir][0], loc[1] + directions[dir][1]


def is_connected(my_map, start, goal):
    open_list = deque()
    closed_list = set()
    open_list.append(start)
    closed_list.add(start)
    while len(open_list) > 0:
        curr = open_list.popleft()
        if curr == goal:
            return True
        for i in range(4):
            next = move(curr, i)
            if my_map[next[0]][next[1]] or next in closed_list:
                continue
            open_list.append(next)
            closed_list.add(next)
    return False


def gen_random_map(size, num_of_obs):
    """Generates a random, fully-connected, square world of size cells per side.
    size        - cells per sided
    num_of_obs  - number of obstacle
    returns     - my_map
    """

    if num_of_obs > size * size or num_of_obs < 0:
        raise ValueError('Improper obstacle obs_density')

    size += 2  # two additional cols and rows for obstacle fences
    my_map = [[False for _ in range(size)] for _ in range(size)]

    # add obstacle fences
    for i in range(size):
        my_map[0][i] = True
        my_map[i][0] = True
        my_map[-1][i] = True
        my_map[i][-1] = True

    i = 0
    while i < num_of_obs:
        obs = (random.randint(0, size - 1), random.randint(0, size - 1))
        if my_map[obs[0]][obs[1]]:
            continue  # this location already has an obstacle
        my_map[obs[0]][obs[1]] = True
        dir1 = 0
        dir2 = 1
        while dir1 < 3 and dir2 < 4:
            start = move(obs, dir1)
            goal = move(obs, dir2)
            if my_map[start[0]][start[1]]:
                dir1 += 1
            elif dir2 <= dir1:
                dir2 = dir1 + 1
            elif my_map[goal[0]][goal[1]]:
                dir2 += 1
            elif is_connected(my_map, start, goal):
                dir1 = dir2
                dir2 += 1
            else:
                my_map[obs[0]][obs[1]] = False
                i -= 1
                break
        i += 1

    return my_map


def gen_random_starts_and_goals(my_map, num_of_agents, random_walk_steps=NUM_WALKS):
    """Generate random start and goal locations by random walk.
    my_map          - binary obstacle maps
    num_of_agents   - number of agents
    """

    size_x = len(my_map)
    size_y = len(my_map[1])
    # Generate the initial positions of the robots
    starts = []
    goals = []
    used4starts = [[False for _ in range(size_y)] for _ in range(size_x)]
    used4goals = [[False for _ in range(size_y)] for _ in range(size_x)]
    while len(starts) < num_of_agents:
        # Generate possible initial and goal positions
        start = (random.randint(0, size_x - 1), random.randint(0, size_y - 1))
        if my_map[start[0]][start[1]] or used4starts[start[0]][start[1]]:
            continue
        curr = start
        i = 0
        while i < random_walk_steps or used4goals[curr[0]][curr[1]]:
            r = random.randint(0, 3)
            next = move(curr, r)
            if my_map[next[0]][next[1]] is False:
                curr = next
                i += 1
        goal = curr
        starts.append(start)
        used4starts[start[0]][start[1]] = True
        goals.append(goal)
        used4goals[goal[0]][goal[1]] = True

    return starts, goals


def save_mapf_instance(filename, my_map, starts, goals):

    mapSize = len(my_map)
    f = open(filename, 'w')
    f.write('{row} {col}\n'.format(row = mapSize, col = mapSize))
    for row in my_map:
        for cell in row:
            if cell:
                f.write('@ ')
            else:
                f.write('. ')
        f.write('\n')
    f.write('{numAgents}\n'.format(numAgents = len(starts)))
    for i in range(len(starts)):
        start = starts[i]
        goal = goals[i]
        f.write('{} {} {} {}\n'.format(start[0], start[1], goal[0], goal[1]))
    f.close()

# Create testing maps
for mapIdx in range(len(MAP_SIZES)):
    mapSize = MAP_SIZES[mapIdx]
    for agentIdx in range(len(NUM_AGENTS)):
        numAgents = NUM_AGENTS[agentIdx]
        if numAgents == max(NUM_AGENTS) and mapSize == min(MAP_SIZES):
            break
        for trialIdx in range(NUM_TRIALS):   
            # Number of obstacles 
            maxObs = math.floor(mapSize * mapSize / 1.5)
            numObstacles = random.randint(0, maxObs)
            # Create map
            testMap = gen_random_map(mapSize, numObstacles)
            # Create starts and goals
            starts, goals = gen_random_starts_and_goals(testMap, numAgents)

            # Output filename
            filename = './instance/' + str(mapSize + 2) + '_' + str(numAgents) + '_' + str(trialIdx) + '.txt'
            save_mapf_instance(filename, testMap, starts, goals)


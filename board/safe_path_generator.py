import math
from heapq import *

# this class holds the secondary graph for finding safe paths that avoid all stones on the board
# it is also responsible for generating those paths using A*

NODES = [(0.5, 0.5), (2, 0.5), (3, 0.5), (4, 0.5), (5.5, 0.5),  # nodes 0-4
         (1.5, 1.5), (2, 1.5), (3, 1.5), (4, 1.5), (4.5, 1.5),  # nodes 5-9
         (0.5, 2),   (1.5, 2), (4.5, 2), (5.5, 2),              # nodes 10-13
         (0.5, 3),   (1.5, 3), (4.5, 3), (5.5, 3),              # nodes 14-17
         (0.5, 4),   (1.5, 4), (4.5, 4), (5.5, 4),              # nodes 18-21
         (1.5, 4.5), (2, 4.5), (3, 4.5), (4, 4.5), (4.5, 4.5),  # nodes 22-26
         (0.5, 5.5), (2, 5.5), (3, 5.5), (4, 5.5), (5.5, 5.5),  # nodes 27-31
         (1.39, -0.6), (4.61, -0.6), (1.39, 6.6), (4.61, 6.6)  # nodes in base, 32 & 33 in AI, 34 & 35 in player
         ]  # node at INDEX has coordinates VALUE
CONNECTIONS = [[1, 10],  [0, 2, 6],    [1, 3],   [2, 4, 8],    [3, 13],   # nodes 0-4
               [6, 11],  [1, 5, 7],    [6, 8],   [3, 7, 9],    [8, 12],   # nodes 5-9
               [0, 11, 14],    [5, 10, 15],  [9, 13, 16],  [4, 12, 17],   # nodes 10-13
               [10, 18],       [11, 19],     [12, 20],     [13, 21],      # nodes 14-17
               [14, 19, 27],   [15, 18, 22], [16, 21, 26], [17, 20, 31],  # nodes 18-21
               [19, 23], [22, 24, 28], [23, 25], [24, 26, 30], [20, 25],  # nodes 22-26
               [18, 28], [23, 27, 29], [28, 29], [25, 29, 31], [21, 30],  # nodes 27-31
               [10], [15], [13], [21]  # nodes in base, 32-35
               ]  # node at INDEX is connected to all nodes in VALUE
ACCESS_POINTS = [[0],       [2],       [4],
                 [0, 5],    [2, 7],    [4, 9],
                 [5],       [7],       [9],
                 [14],      [14, 15],  [15],
                 [16],      [16, 17],  [17],
                 [22],      [24],      [26],
                 [22, 27],  [24, 29],  [26, 31],
                 [27],      [29],      [31],
                 [32], [33], [32], [33], [32], [33], [33], [33], [32],  # AI base, in order of access
                 [35], [34], [35], [34], [35], [34], [34], [34], [35]   # player base, in order of access
                 ]  # field at INDEX is connected to all nodes in VALUE

# astar() based on from https://code.activestate.com/recipes/578919-python-a-pathfinding-with-binary-heap/
# released under the MIT License, retrieved 18.10.2017

def heuristic(i_a, i_b):
    a = NODES[i_a]
    b = NODES[i_b]
    return math.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)

def astar(start, goal):  # A* search algorithm
    close_set = set()
    came_from = {}
    gscore = {start: 0}
    fscore = {start: heuristic(start, goal)}
    oheap = []

    heappush(oheap, (fscore[start], start))

    while oheap:
        current = heappop(oheap)[1]
        if current == goal:  # goal reached, retrace steps and output path
            data = []
            score = gscore.get(current, 20)
            while current in came_from:
                data.append(current)
                current = came_from[current]
            data.append(0)
            data.reverse()
            return data, score
        close_set.add(current)  # add current node to close_set, as all neighbors will have been evaluated
        for neighbor in CONNECTIONS[current]:
            tentative_g_score = gscore[current] + heuristic(current, neighbor)  # g-score of neighbor using current path
            if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):  # neighbor already closed w/ lower g-score
                continue
            if tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1] for i in oheap]:  # better g-score or new node
                came_from[neighbor] = current
                gscore[neighbor] = tentative_g_score
                fscore[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                heappush(oheap, (fscore[neighbor], neighbor))
    return False  # only returned if all nodes evaluated but none reached goal

def generate(start_ind, end_ind):
    if start_ind == -1 or end_ind == -1:
        raise RuntimeError('Position in base must be resolved first')
    best_path = []
    mind_dist = float('inf')
    for s in ACCESS_POINTS[start_ind]:
        for e in ACCESS_POINTS[end_ind]:
            path, dist = astar(s, e)
            if dist < mind_dist:
                mind_dist = dist
                best_path = []
                for p in path:
                    best_path.append(NODES[p])
    return best_path

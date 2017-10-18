import math
from heapq import *

# this class holds the secondary graph for finding safe paths that avoid all stones on the board
# it is also responsible for generating those paths using A*

NODES = [(), ()]  # node at INDEX has coordinates VALUE  TODO
CONNECTIONS = [[], []]  # node at INDEX is connected to all nodes in VALUE  TODO
ACCESS_POINTS = [[], []]  # field at INDEX is connected to all nodes in VALUE  TODO

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
    best_path = []
    mind_dist = float('inf')
    for s in ACCESS_POINTS[start_ind]:
        for e in ACCESS_POINTS[end_ind]:
            p, dist = astar(s, e)
            if dist < mind_dist:
                mind_dist = dist
                best_path = p
    return best_path

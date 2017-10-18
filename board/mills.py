#!/usr/bin/env python
import motors
import input
import magnet
import ai
import time
import math
import safe_path_generator as SPG
import RPi.GPIO as GPIO

COLOR_AI = 1
COORDS = [(0,0), (3,0), (6,0),    (1,1), (1,3), (1,5),    (2,2), (2,3), (2,4),    (3,0), (3,1), (3,2),    (3,4), (3,5), (3,6),    (4,2), (4,3), (4,4),    (5,1), (5,3), (5,5),    (6,0), (6,3), (6,6)]
BASE_COORDS = [[(6.22,6.6) for x in range(9)],  #BASE_PLAYER
               [(-0.22,-0.6) for x in range(9)]]  #BASE_AI #TODO

old_board = [0] * 24
pieces_player = 9
pieces_ai = 9


def resolve(i, context_board, base_color):
    if i == -1: # -1 corresponds to a position in the base
        if base_color == COLOR_AI:
            base_ind = pieces_ai - 1
        else:
            base_ind = pieces_player - 1
        return BASE_COORDS[1 if base_color == COLOR_AI else 0][base_ind], base_color
    else:
        return COORDS[i], context_board[i]

def dist(a, b):
    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)
def distance_to_line_seg(p0, s, t):
    # Line segment st as part of line: s + x*(t-s)
    # Find l2 as (t-s)^2
    l2 = (s[0] - t[0])**2 + (s[1] - t[1])**2
    if l2 == 0:  # s = t
        return dist(p0, s)
    # Find x as dot(p - s, t - s) / l2, clamp to [0,1] -> inside st
    x = ((p0[0] - s[0]) * (t[0] - s[0]) + (p0[1] - s[1]) * (t[1] - s[1])) / l2
    x = max(0, min(1, x))
    # Calc proj. point -> s + x*(t-s)
    _p = (s[0] + x * (t[0] - s[0]), s[1] + x * (t[1] - s[1]))
    return dist(p0, _p)

def isUnblocked(_board, s, t):
    for i in range(len(_board)):
        if _board[i] == 0:
            continue
        _pos, _ = resolve(i, _board, COLOR_AI)
        if distance_to_line_seg(_pos, s, t) < 0.4:
            return False
    return True

def getShortSafePath(_board, start, target):
    best_states = []
    min_dist = float('inf')
    _board[start] = 0  # no collision tith stone that should be moved

    safe_path = [COORDS[start]]
    safe_path.extend(SPG.generate(start, target))  # list of tuples, first = start, last = target
    safe_path.append(COORDS[target])
    l = len(safe_path)-2
    for i in range(2 ** l):  # for every possible combination of active vertices
        m = i
        isActive = [True]  # holds state of every vertex, first always active
        for j in range(l-1, -1, -1):  # for every middle vertex
            k = int(m / 2 ** j)
            m -= k * 2 ** j
            isActive.append(k==1)
        isActive.append(True)  # last always active

        valid = True
        tot_dist = 0
        for j in range(l+1):  # for every vertex
            next_active = -1
            for k in range(j+1, len(safe_path)):
                if isActive[k]:
                    next_active = k
                    break
            valid = valid and isUnblocked(_board, safe_path[j], safe_path[next_active])
            tot_dist += math.sqrt((safe_path[j][0] - safe_path[next_active][0])**2
                                  + (safe_path[j][1] - safe_path[next_active][1])**2)

        if valid and tot_dist < min_dist:
            min_dist = tot_dist
            best_states = isActive

    avoid_path = []
    for i, val in enumerate(best_states):
        if val:
            avoid_path.append(safe_path[i])
    return avoid_path

def shutdown():
    input.shutdown()
    motors.shutdown()
    magnet.shutdown()
    GPIO.cleanup()

try:
    print('Resetting motors...')
    motors.reset()
    while True:
        print('Checking board...')
        board = input.readBoard()
        if not old_board == board:
            print('read board: ' + str(board))
            print('found changes, calculating move')

            if pieces_player > 0:  # ASSUME player uses all pieces from his storage before playing normally
                pieces_player -= 1

            _, moves = ai.calcMove(board, COLOR_AI, pieces_ai, pieces_player)
            for move in moves:
                start = move[0]
                dest = move[1]
                print('move: ', move[0], 'to', move[1])

                # resolve coords of start and dest & color of piece
                c1, color = resolve(start, board, COLOR_AI)  # can only move pieces out of own base
                c2, _ = resolve(dest, board, -COLOR_AI)  # can only put pieces in opponents base

                # move piece from start to dest
                motors.goTo(c1[0], c1[1])
                magnet.turnOn(color)
                path = getShortSafePath(board, start, dest)
                for pos in path:
                    motors.goTo(pos[0], pos[1])
                magnet.turnOff()
                time.sleep(0.5)
            motors.goTo(motors.RESET_POS[0], motors.RESET_POS[1])
            motors.reset()
            old_board = input.readBoard()
        else:
            time.sleep(2)
except KeyboardInterrupt:
    shutdown()

#!/usr/bin/env python
import motors
import input
import magnet
import ai
import time
import math
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


def distance_to_line(p0, s, t):
    x_diff = t[0] - s[0]
    y_diff = t[1] - s[1]
    num = abs(y_diff * p0[0] - x_diff * p0[1] + t[0] * s[1] - t[1] * s[0])
    den = math.sqrt(y_diff ** 2 + x_diff ** 2)
    return num / den

def isUnblocked(_board, s, t):
    for stone in _board:
        pos = resolve(stone, _board, COLOR_AI)
        return distance_to_line(pos, s, t) > 3

def getSafePath(start, target):  # TODO
    return [start, ..., target]

def getShortSafePath(_board, start, target):
    best_states = []
    min_dist = float('inf')

    safe_path = getSafePath(start, target)  # list of tuples, first = start, last = target
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
            for k in range(j+1, l):
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
                path = getShortSafePath(board, c1, c2)
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

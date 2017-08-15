#!/usr/bin/env python
import motors
import input
import magnet
import ai
import time

COLOR_AI = 1
COORDS = [] #TODO
BASE_COORDS = [] #TODO

old_board = [0] * 24
pieces_player = 9
pieces_ai = 9


def resolve(i, board, base_color):
    if i == -1:
        if base_color == COLOR_AI:
            base_ind = pieces_ai - 1
        else:
            base_ind = pieces_player - 1
        return BASE_COORDS[base_color][base_ind], base_color
    else:
        return COORDS[i], board[i]

while True:
    print('reading...')
    board = input.readBoard()
    if not old_board == board:
        print('found changes, calculating move')

        if pieces_player > 0:  # ASSUME player uses all pieces from his storage before playing normally
            pieces_player -= 1

        moves = ai.calcMove(board, COLOR_AI, pieces_ai, pieces_player)
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
            motors.goTo(c2[0], c2[1])
            magnet.turnOff()
    else:
        time.sleep(2)

#!/usr/bin/env python
# All original code, based on Alpha-Beta algorithm

import numpy as np
import morris
import time

def step(board, color=1):
    startTime = time.perf_counter()
    
    depth = 5
    bestBoard, _, reward, terminal = alphaBeta(board, color, depth)
    
    print('Board analyzed, depth: %d, time: %f' % (depth, time.perf_counter() - startTime))
    
    return bestBoard, reward, terminal
    
def alphaBeta(board, color, depth): # returns board (state of board after best move), score (value of board after best move), reward for that move, terminal if that move ends the game
    if depth <= 0:
        return board, value(board, color=color) - value(board, color=-color), 0, False # reward and terminal unknown
    else:
        worstHisScore = infinity
        bestBoard = None
        reward = 0
        terminal = False
        for move: # TODO !!!!!
            board_after = move(board) # create board and execute move
            _, hisScore, _, _ = alphaBeta(board_after, -color, depth-1) # evaluate position for opponent, minimize his advantage
            if hisScore < worstHisScore:
                bestBoard = board_after
                worstHisScore = score
            # TODO !!!!!
            reward = 0
            terminal = False
        return bestBoard, -worstHisScore, reward, terminal # return board which was worst for opponent, return advantage over opponent = -(his score)
    
def value(board, color=1):
    value = 0
    fs = [morris.indexAbove, morris.indexBelow, morris.indexLeft, morris.indexRight]
    
    mills = 0
    for i in range(len(board)):
        if board[i] == color:
            # count pieces
            value += 1
            # count moves
            for f in fs:
                index = f(i)
                if index != -1:
                    if board[index] == 0:
                        value += 0.2
            # count pieces in mills
            if morris.isInMill(board, i):
                mills += 1
    
    # count mills
    if mills % 3 != 0: # round up to next multiple of 3
        mills += 3 - (mills % 3)
    mills /= 3 # because we count three pieces per mill (unless they intersect, but that's why we rounded up - it's not perfect, I know)
    value += 5 * mills
    
    return value
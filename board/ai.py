#!/usr/bin/env python
# All original code, based on Alpha-Beta algorithm
import numpy as np
import time

# SETTINGS
LOG = False # Enables logging of timeTaken's

TAKE_PIECE_REWARD = 0.2
WIN_REWARD = 1

# UTILITY DUNCTIONS
# Lookup table for what fields are above others, nicer and more readable than if's
above_arr = [-1, -1, -1, -1, 1, -1, -1, 4, -1, 0, 3, 6, 8, 5, 2, 11, -1, 12, 10, 16, 13, 9, 19, 14]
def indexAbove(i):
    return above_arr[i]
def indexBelow(i):
    try:
        return above_arr.index(i)
    except ValueError:
        return -1
def indexLeft(i):
    if i % 3 == 0:
        return -1
    else:
        return i-1
def indexRight(i):
    if i % 3 == 2:
        return -1
    else:
        return i+1
def isInMill(board, i):
    if i == -1:
        return False
    else:
        return (safeGet(board, indexAbove(i)) == safeGet(board, indexAbove(indexAbove(i))) == board[i] != 2) or \
               (safeGet(board, indexAbove(i)) == safeGet(board, indexBelow(i)) == board[i] != 2) or \
               (safeGet(board, indexBelow(i)) == safeGet(board, indexBelow(indexBelow(i))) == board[i] != 2) or \
               (safeGet(board, indexLeft(i)) == safeGet(board, indexLeft(indexLeft(i))) == board[i] != 2) or \
               (safeGet(board, indexLeft(i)) == safeGet(board, indexRight(i)) == board[i] != 2) or \
               (safeGet(board, indexRight(i)) == safeGet(board, indexRight(indexRight(i))) == board[i] != 2)
def safeGet(board, i):
    if i < 0 or i >= len(board):
        return 2
    return board[i]
# END UTILITY FUNCTIONS


def calcMove(board, color, pieces_self, pieces_opponent):
    #startTime = time.perf_counter()
    depth = 3
    
    bestBoard, _, reward, terminal, movesDone = step(np.array(board), color, depth, pieces_self, pieces_opponent)
    #timeTaken = time.perf_counter() - startTime
    
    #print('Board analyzed, depth: %d, time: %f seconds' % (depth, timeTaken)) # DEBUG
    
    if LOG:
        with open('log.csv', 'a') as f:
            f.write('\n%s, %f' % (depth, timeTaken))
    
    return bestBoard, movesDone

def step(board, color, depth, pieces_self, pieces_opponent): # returns board (state of board after best move), score (value of board after best move), reward for that move, terminal if that move ends the game
    if depth <= 0:
        return board, value(board, color=color) - value(board, color=-color), 0, False, [] # reward, terminal and moves won't be used anyway
    else:
        worstHisScore = float("inf")
        bestBoard = board
        reward = -WIN_REWARD # outcome if no possible move can be found
        terminal = True
        movesDone = []
        for m in moves(board, color, pieces_self):
            board_after = np.array(m.new_board)
            requiredMoves = m.moves
            _, hisScore, _, _, _ = step(board_after, -color, depth-1, pieces_opponent, pieces_self-1)
            # evaluate position for opponent, minimize his advantage
            
            r = 0
            t = False
            num_pieces_self = len(board_after[board_after == color])
            num_pieces_opponent = len(board_after[board_after == -color])
            if num_pieces_self < 3 and pieces_self <= 0: # probably unneccessary
                r = -WIN_REWARD
                t = True
            elif num_pieces_opponent < 3 and pieces_opponent <= 0:
                r = WIN_REWARD
                t = True
            elif num_pieces_opponent < len(board[board == -color]):
                r = TAKE_PIECE_REWARD
            elif num_pieces_self < len(board[board == color]): # probably unneccessary
                r = -TAKE_PIECE_REWARD
            
            if hisScore < worstHisScore or r == WIN_REWARD:
                bestBoard = board_after
                worstHisScore = hisScore
                movesDone = requiredMoves
                reward = r
                terminal = t
            if r == WIN_REWARD:
                break
            
        return bestBoard, -worstHisScore, reward, terminal, movesDone
        # return board which was worst for opponent, return advantage over opponent = -(his score)

class change:
    moves = [(-1,-1)]
    new_board = []

# noinspection PyTypeChecker
def moves(board, color, pieces_self):
    boards = np.array([], dtype=object)

    if pieces_self > 0: # can set down anywhere
        for i, val in enumerate(board):  # for each field, if unoccupied, set down piece and add new_board
            if val == 0:
                new_board = [x for x in board]
                new_board[i] = color
                def_move = (-1, i)  # move piece from base to i

                if isInMill(new_board, i):  # if mill closed, instead list all possibilities for taking pieces
                    mill_boards, mill_moves = moves_on_mill_closed(new_board, color)
                    for k in range(len(mill_boards)):
                        move = change()
                        move.moves = [def_move, (mill_moves[k][0], mill_moves[k][1])]
                        move.new_board = mill_boards[k]
                        boards = np.append(boards, move)
                else:
                    move = change()
                    move.moves = [def_move]  # move piece from base to i
                    move.new_board = new_board
                    boards = np.append(boards, move)
    elif len(board[board == color]) > 3: # can't jump
        fs = [indexAbove, indexBelow, indexLeft, indexRight]
        for i, val in enumerate(board): # for each field, if own piece, add new_board for all possible moves
            if val == color:
                for f in fs:
                    if f(i) == -1:
                        continue
                    if board[f(i)] == 0:
                        new_board = [x for x in board]
                        new_board[i] = 0
                        new_board[f(i)] = color
                        def_move = (i, f(i))  # move piece from i to f(i)

                        if isInMill(new_board, f(i)):  # if mill closed, instead list all possibilities for taking pieces
                            mill_boards, mill_moves = moves_on_mill_closed(new_board, color)
                            for k in range(len(mill_boards)):
                                move = change()
                                move.moves = [def_move, (mill_moves[k][0], mill_moves[k][1])]
                                move.new_board = mill_boards[k]
                                boards = np.append(boards, move)
                        else:
                            move = change()
                            move.moves = [def_move]  # move piece from base to i
                            move.new_board = new_board
                            boards = np.append(boards, move)
    else: # can jump
        for i, val in enumerate(board): # for each field, if own piece, add new_board for all unoccupied fields
            if val == color:
                for j, val2 in enumerate(board):
                    if val2 == 0: # also catches i==j because color!=0
                        new_board = [x for x in board]
                        new_board[i] = 0
                        new_board[j] = color
                        def_move = (i, j)  # move piece from i to j

                        if isInMill(new_board, j):  # if mill closed, instead list all possibilities for taking pieces
                            mill_boards, mill_moves = moves_on_mill_closed(new_board, color)
                            for k in range(len(mill_boards)):
                                move = change()
                                move.moves = [def_move, (mill_moves[k][0], mill_moves[k][1])]
                                move.new_board = mill_boards[k]
                                boards = np.append(boards, move)
                        else:
                            move = change()
                            move.moves = [def_move]
                            move.new_board = new_board
                            boards = np.append(boards, move)

    # print('calculated %d possible moves:' % len(boards))
    # print(boards)
    return boards


def moves_on_mill_closed(board, color):
    allowed = np.array([], dtype=np.int16)
    allowedMoves = np.array([], dtype=np.int16)
    disallowed = np.array([], dtype=np.int16)
    disallowedMoves = np.array([], dtype=np.int16)
    for k, val3 in enumerate(board):
        if val3 == -color:
            new_board = [x for x in board]
            new_board[k] = 0
            if isInMill(board, k):  # save taking stones out of mills separately
                disallowed = np.append(disallowed, new_board)
                disallowedMoves = np.append(disallowedMoves, (k, -1))  # move k to base
            else:
                allowed = np.append(allowed, new_board)
                allowedMoves = np.append(allowedMoves, (k, -1))  # move k to base
    if len(allowed) <= 0:
        num = int(len(disallowed)/24)
        return disallowed.reshape(num, 24), disallowedMoves.reshape(num, 2)
    else:
        num = int(len(allowed)/24)
        return allowed.reshape(num, 24), allowedMoves.reshape(num, 2) # no allowed moves -> all moves allowed


def value(board, color=1):
    v = 0
    fs = [indexAbove, indexBelow, indexLeft, indexRight]
    
    mills = 0
    for i in range(len(board)):
        if board[i] == color:
            # count pieces
            v += 3
            # count moves
            for f in fs:
                index = f(i)
                if index != -1:
                    if board[index] == 0:
                        v += 0.1
            # count pieces in mills
            if isInMill(board, i):
                mills += 1
    
    # count mills
    if mills % 3 != 0:  # round up to next multiple of 3
        mills += 3 - (mills % 3)
    mills /= 3 # because we count APPROXIMATELY three pieces per mill
    v += 1 * mills
    
    return v

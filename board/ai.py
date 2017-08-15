#!/usr/bin/env python
# All original code, based on Alpha-Beta algorithm
import numpy as np
import morris
import time

# SETTINGS
LOG = False # Enables logging of timeTaken's


# TODO MUST RETURN MOVES, NOT BOARD!
def calcMove(board, color, pieces_self, pieces_opponent):
    global last_times
    
    startTime = time.perf_counter()
    depth = 3
    
    bestBoard, _, reward, terminal = step(board, color, depth, pieces_self, pieces_opponent)
    timeTaken = time.perf_counter() - startTime
    
    #print('Board analyzed, depth: %d, time: %f seconds' % (depth, timeTaken)) # DEBUG
    
    if LOG:
        with open('log.csv', 'a') as f:
            f.write('\n%s, %f' % (depth, timeTaken))
    
    return bestBoard
    
def step(board, color, depth, pieces_self, pieces_opponent): # returns board (state of board after best move), score (value of board after best move), reward for that move, terminal if that move ends the game
    if depth <= 0:
        return board, value(board, color=color) - value(board, color=-color), 0, False # reward and terminal won't be used anyway
    else:
        worstHisScore = float("inf")
        bestBoard = board
        reward = -morris.WIN_REWARD # outcome if no possible move can be found
        terminal = True
        for board_after in moves(board, color, pieces_self):
            _, hisScore, _, _ = step(board_after, -color, depth-1, pieces_opponent, pieces_self-1) # evaluate position for opponent, minimize his advantage
            
            r = 0
            t = False
            num_pieces_self = len(board_after[board_after == color])
            num_pieces_opponent = len(board_after[board_after == -color])
            if num_pieces_self < 3 and pieces_self <= 0: # probably unneccessary
                r = -morris.WIN_REWARD
                t = True
            elif num_pieces_opponent < 3 and pieces_opponent <= 0:
                r = morris.WIN_REWARD
                t = True
            elif num_pieces_opponent < len(board[board == -color]):
                r = morris.TAKE_PIECE_REWARD
            elif num_pieces_self < len(board[board == color]): # probably unneccessary
                r = -morris.TAKE_PIECE_REWARD
            
            if hisScore < worstHisScore or r == morris.WIN_REWARD:
                bestBoard = board_after
                worstHisScore = hisScore
                reward = r
                terminal = t
            if r == morris.WIN_REWARD:
                break
            
        return bestBoard, -worstHisScore, reward, terminal # return board which was worst for opponent, return advantage over opponent = -(his score)

def moves(board, color, pieces_self):
    boards = np.array([], dtype=np.int16)
    
    if pieces_self > 0: # can set down anywhere
        for i, val in enumerate(board): # for each field, if unoccupied, set down piece and add new_board
            if val == 0:
                new_board = [x for x in board]
                new_board[i] = color
                
                if morris.isInMill(new_board, i): # if mill closed, also list all possibilities for taking pieces
                    boards = np.append(boards, moves_on_mill_closed(new_board, color))
                else:
                    boards = np.append(boards, new_board)
    elif len(board[board == color]) > 3: # can't jump
        fs = [morris.indexAbove, morris.indexBelow, morris.indexLeft, morris.indexRight]
        for i, val in enumerate(board): # for each field, if own piece, add new_board for all possible moves
            if val == color:
                for f in fs:
                    if f(i) == -1:
                        continue
                    if board[f(i)] == 0:
                        new_board = [x for x in board]
                        new_board[i] = 0
                        new_board[f(i)] = color
                        
                        if morris.isInMill(new_board, f(i)): # if mill closed, also list all possibilities for taking pieces
                            boards = np.append(boards, moves_on_mill_closed(new_board, color))
                        else:
                            boards = np.append(boards, new_board)
    else: # can jump
        for i, val in enumerate(board): # for each field, if own piece, add new_board for all unoccupied fields
            if val == color:
                for j, val2 in enumerate(board):
                    if val2 == 0: # also catches i==j because color!=0
                        new_board = [x for x in board]
                        new_board[i] = 0
                        new_board[j] = color
                        
                        if morris.isInMill(new_board, j): # if mill closed, also list all possibilities for taking pieces
                            boards = np.append(boards, moves_on_mill_closed(new_board, color))
                        else:
                            boards = np.append(boards, new_board)
    
    num_moves = int(len(boards)/24)
    #print('calculated %d possible moves:' % num_moves)
    #print(boards)
    return boards.reshape(num_moves, 24)
    
def moves_on_mill_closed(board, color):
    allowed = np.array([], dtype=np.int16)
    disallowed = np.array([], dtype=np.int16)
    for k, val3 in enumerate(board):
        if val3 == -color:
            new_board = [x for x in board]
            new_board[k] = 0
            if morris.isInMill(board, k): # save taking stones out of mills separately
                disallowed = np.append(disallowed, new_board)
            else:
                allowed = np.append(allowed, new_board)
    if len(allowed) <= 0: # no allowed moves -> all moves allowed
        return disallowed
    else:
        return allowed
def value(board, color=1):
    v = 0
    fs = [morris.indexAbove, morris.indexBelow, morris.indexLeft, morris.indexRight]
    
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
            if morris.isInMill(board, i):
                mills += 1
    
    # count mills
    if mills % 3 != 0: # round up to next multiple of 3
        mills += 3 - (mills % 3)
    mills /= 3 # because we count three pieces per mill (unless they intersect, but that's why we rounded up - it's not perfect, I know)
    v += 1 * mills
    
    return v
#!/usr/bin/env python
import motors
import input
import magnet
import ai
import time
import math
import safe_path_generator as SPG
import pygame
import RPi.GPIO as GPIO

pygame.mixer.init()

COLOR_AI = 1
COORDS = [(0,0), (3,0), (6,0),    (1,1), (1,3), (1,5),    (2,2), (2,3), (2,4),    (3,0), (3,1), (3,2),    (3,4), (3,5), (3,6),    (4,2), (4,3), (4,4),    (5,1), (5,3), (5,5),    (6,0), (6,3), (6,6)]
BASE_COORDS = [[(6.22-(6.44/8*(8-x)),6.6) for x in range(9)],  #BASE_PLAYER
               [(-0.22+(6.44/8*(8-x),-0.6) for x in range(9)]]  #BASE_AI

old_board = [0] * 24
pieces_player = 9
pieces_ai = 9


def resolve(i, context_board, base_color):
    if i == -1: # -1 corresponds to a position in the base
        if base_color == COLOR_AI:
            base_ind = pieces_ai
        else:
            base_ind = pieces_player
        return BASE_COORDS[1 if base_color == COLOR_AI else 0][base_ind], base_color
    else:
        return COORDS[i], context_board[i]

def getShortSafePath(_board, start, target):
    start_pos, _ = resolve(start, _board, COLOR_AI)
    target_pos, _ = resolve(target, _board, -COLOR_AI)
    safe_path = [start_pos]
    safe_path.extend(SPG.generate(start, target))  # list of tuples, first = start, last = target
    safe_path.append(target_pos)
    
    print('safe path from %i to %i is: %s' % (start, target, str(safe_path)))
    return safe_path

def reset():
    # Resets all pieces to the base, clears any records of previous boards
    time.sleep(2)
    print('Resetting the board')
    # TODO

def shutdown():
    input.shutdown()
    motors.shutdown()
    magnet.shutdown()
    GPIO.cleanup()

def count(_board, _color):
    num = 0
    for val in _board:
        if val == _color:
            num += 1
    return num

# These methods play a sound, wait for it to finish and then wait 0.5s more
def play_sound(path):
    print('playing sound: %s' % path)
    pygame.mixer.music.load(path)
    pygame.mixer.music.play()

try:
    print('Resetting motors...')
    motors.reset()
    while True:
        print('Checking board...')
        board = input.readBoard()
        should_move = False
        if old_board != board:
            # A move is over when a stone has been moved -> same number of pieces in phase 2/3
            # or when a stone has been placed -> number of player pieces increased by 1
            # If a mill has just been closed (new stone isInMill), after a COLOR_AI piece has been removed
            # If one color now only has two pieces left, the game is over -> clean board
            num_ai_old = count(old_board, COLOR_AI)
            num_ai = count(board, COLOR_AI)
            num_pl_old = count(old_board, -COLOR_AI)
            num_pl = count(board, -COLOR_AI)
            pl_move_dest = -1
            for i, v in enumerate(board):
                if old_board[i] == 0 and v == -COLOR_AI:  # player piece added
                    pl_move_dest = i
            if num_ai < 3 and pieces_ai == 0:  # AI just lost
                print('Suppose I\'ve lost :(')
                play_sound('../sounds/clap.wav')
                reset()
                continue
            if ai.isInMill(board, pl_move_dest):  # If a mill was closed, the move ends when one num_ai decreases by 1
                should_move = num_ai == num_ai_old-1
                if should_move:
                    print('Found closed mill on field %i, AI piece removed' % pl_move_dest)
            else:  # otherwise, both players must have the same number of pieces as before
                phase_one = pieces_player != 0 and pieces_ai != 0
                should_move = ((not phase_one) and num_pl == num_pl_old and num_ai == num_ai_old) \
                               or (phase_one and num_pl == num_pl_old+1 and num_ai == num_ai_old)
                if should_move:
                    print('Found move to %i without any closed mills' % pl_move_dest)
        if should_move:
            print('board: ' + str(board))
            play_sound('../sounds/ping.wav')
            print('calculating move... p_ai=%i p_pl=%i' % (pieces_ai, pieces_player))

            if pieces_player > 0:  # ASSUME player uses all pieces from their storage before playing normally
                pieces_player -= 1
            if pieces_ai > 0:  # ASSUME AI uses all pieces from its storage before playing normally
                pieces_ai -= 1

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
            if count(old_board, -COLOR_AI) < 3 and pieces_player == 0:  # AI just won
                play_sound('../sounds/fanfare.wav')
                reset()
                continue
        else:
            time.sleep(1)
except KeyboardInterrupt:
    shutdown()

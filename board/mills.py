#!/usr/bin/env python
import ai
import time
import safe_path_generator as SPG
try:
    import RPi.GPIO as GPIO
    import motors
    import input
    import magnet
    TEST_MODE = False
except ImportError:
    TEST_MODE = True
import sys
import pygame

pygame.mixer.init()

COLOR_AI = 1
COORDS = [(0,0), (0,3), (0,6),    (1,1), (1,3), (1,5),    (2,2), (2,3), (2,4),    (3,0), (3,1), (3,2),    (3,4), (3,5), (3,6),    (4,2), (4,3), (4,4),    (5,1), (5,3), (5,5),    (6,0), (6,3), (6,6)]
order_arr = [[8, 2, 0, 4, 6, 5, 1, 3, 7].index(x) for x in range(9)]  # which base field is accessed when (the first at time 8, the second at time 2)
COORDS.extend([(-0.22+(6.44/8*x), -0.64) for x in order_arr])  # BASE_AI from 24 - 32
COORDS.extend([(6.22-(6.44/8*x), 6.64) for x in order_arr])  # BASE_PLAYER from 33 - 41

shutdownPin = 11
ledPin = 3

old_board = [0] * 24
pieces_player = 9
pieces_taken = 0
pieces_ai = 9

# Returns the updated board index referring to a specific position in the base instead of the base in general
def resolve_base(_i, base_color):
    if _i != -1:  # no effect on normal fields
        return _i
    if base_color == COLOR_AI:
        return 24 + 9 - pieces_ai
    else:
        # list: where to put taken pieces first in player base (such that all pieces can be placed in the worst case)
        return 33 + [2, 4, 6, 5, 3, 1, 0][pieces_taken]
def resolve(_i, context_board, base_color):
    global pieces_player, pieces_ai
    if _i == -1:  # -1 corresponds to a position in the base
        return COORDS[resolve_base(_i, base_color)], base_color
    else:
        return COORDS[_i], context_board[_i]

def getShortSafePath(_board, start, target):
    if target == -1 or start == -1:
        raise RuntimeError('Position in base must be resolved first')
    start_pos = COORDS[start]
    target_pos = COORDS[target]
    safe_path = [start_pos]
    safe_path.extend(SPG.generate(start, target))  # list of tuples, first = start, last = target
    safe_path.append(target_pos)
    
    print('safe path from %i to %i is: %s' % (start, target, str(safe_path)))
    return safe_path

def reset():
    global pieces_player, pieces_ai
    # Resets all pieces to the base, clears any records of previous boards
    time.sleep(2)
    print('Resetting the board')
    _board = input.readBoard()
    for _i, val in _board:
        if val != 0:
            _pos, _ = resolve(_i, _board, COLOR_AI)
            _dest, _ = resolve(-1, _board, val)
            if val == COLOR_AI:
                pieces_ai += 1
            else:
                pieces_player += 1
            motors.goTo(_pos[0], _pos[1])
            magnet.turnOn(val)
            _path = getShortSafePath(board, start, _dest)
            for p in _path:
                motors.goTo(p[0], p[1])
            magnet.turnOff()
            time.sleep(0.5)

running = True
def shutdown(channel=0, full=True):
    if running:
        return
    print("Shutting down...")
    input.shutdown()
    motors.shutdown()
    magnet.shutdown()
    GPIO.output(ledPin, GPIO.LOW)
    if full:
        sys.exit(1)
    else:
        sys.exit(0)

def count(_board, _color):
    num = 0
    for val in _board:
        if val == _color:
            num += 1
    return num

# These methods play a sound, wait for it to finish and then wait 0.5s more
def play_sound(_path):
    print('playing sound: %s' % _path)
    pygame.mixer.music.load(_path)
    pygame.mixer.music.play()

if __name__ == "__main__" and not TEST_MODE:
    try:
        GPIO.setup(ledPin, GPIO.OUT)
        GPIO.output(ledPin, GPIO.HIGH)
        GPIO.setup(shutdownPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(shutdownPin, GPIO.RISING, callback=shutdown)

        print('Resetting motors...')
        motors.reset()
        while True:
            running = False
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
                running = True
                print('board: ' + str(board))
                play_sound('../sounds/ping.wav')
                print('calculating move... p_ai=%i p_pl=%i' % (pieces_ai, pieces_player))

                if pieces_player > 0:  # ASSUME player uses all pieces from their storage before playing normally
                    pieces_player -= 1

                old_board, moves = ai.calcMove(board, COLOR_AI, pieces_ai, pieces_player)
                for move in moves:
                    start = move[0]
                    dest = move[1]
                    print('move: ', move[0], 'to', move[1])

                    # resolve coords of start and dest & color of piece
                    c1, color = resolve(start, board, COLOR_AI)  # can only move pieces out of own base
                    c2, _ = resolve(dest, board, COLOR_AI)  # can only put pieces in opponents base

                    # move piece from start to dest
                    motors.goTo(c1[0], c1[1])
                    magnet.turnOn(color)
                    if start == -1 or count(board, COLOR_AI) <= 3 or dest == -1:
                        path = getShortSafePath(board, resolve_base(start, COLOR_AI), resolve_base(dest, -COLOR_AI))
                    else:
                        path = [c1, c2]
                    for pos in path:
                        motors.goTo(pos[0], pos[1])
                    magnet.turnOff()
                    if dest == -1:  # after piece has been moved to the player's base, we can update pieces_taken
                        pieces_taken += 1
                    time.sleep(0.5)
                motors.goTo(0, 0)
                motors.reset()

                if pieces_ai > 0:  # ASSUME AI uses all pieces from its storage before playing normally
                    pieces_ai -= 1

                #old_board = input.readBoard()
                print("board: " + str(old_board))
                if count(old_board, -COLOR_AI) < 3 and pieces_player == 0:  # AI just won
                    play_sound('../sounds/fanfare.wav')
                    reset()
                    continue
                running = False
            else:
                time.sleep(1)
    except KeyboardInterrupt:
        shutdown(full=False)

#!/usr/bin/env python
import pygame
import ai, mills

COLOR_AI = 1
pieces_ai = 9
pieces_player = 9

RESET_POS = (-0.22, -0.64)

live_path = [RESET_POS]

try:
    # PLAYER MOVE
    board = [0 for i in range(24)]
    _start = int(input("Start: "))
    _dest = int(input("Dest: "))
    if ai.isInMill(board, _dest):
        _take = int(input("Take: "))
    else:
        _take = -1
    board[_start] = 0
    board[_dest] = -COLOR_AI
    if _take != -1:
        board[_take] = 0
    pieces_player = max(0, pieces_player-1)

    # AI RESPONSE
    _, moves = ai.calcMove(board, COLOR_AI, pieces_ai, pieces_player)
    pieces_ai = max(0, pieces_ai-1)
    # SHOW EXECUTION PATH
    for move in moves:
        start = move[0]
        dest = move[1]
        print('move: ', move[0], 'to', move[1])

        # resolve coords of start and dest & color of piece
        c1, color = mills.resolve(start, board, COLOR_AI)  # can only move pieces out of own base
        c2, _ = mills.resolve(dest, board, COLOR_AI)  # can only put pieces in opponents base

        # move piece from start to dest
        live_path.append((c1,c2))
        #magnet.turnOn(color)
        if start == -1 or mills.count(board, COLOR_AI) <= 3 or dest == -1:
            path = mills.getShortSafePath(board, mills.resolve_base(start, COLOR_AI), resolve_base(dest, -COLOR_AI))
        else:
            path = [c1, c2]
        for pos in path:
            live_path.append(pos)
        # WAIT
        input("ENTER to continue...")
        # CLEAR PATH
        tmp = live_path[-1]
        live_path = [tmp]
    live_path.append((0,0))
    live_path.append(RESET_POS)
except KeyboardInterrupt:
    print('Interrupted!')
    pygame.quit()
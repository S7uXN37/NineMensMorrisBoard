#!/usr/bin/env python
import pygame, math, time
import ai, mills
import safe_path_generator as SPG

board = [0 for i in range(24)]
board.extend([1 for i in range(9)])
board.extend([-1 for i in range(9)])

RESET_POS = (-0.22, -0.64)

live_path = [RESET_POS]
text_box = "Welcome"

pygame.init()
size = 800
screen = pygame.display.set_mode((size,size))
myfont = pygame.font.SysFont("monospace", 18, bold=True)

def convert(p):
    x = (1 + p[0]) * size/8
    y = (1 + p[1]) * size/8
    return (int(x), int(y))

def draw():
    # BACKGROUND
    screen.fill((30,30,30))
    # LINES
    for i in range(3):
        pygame.draw.line(screen, (50,50,50), convert((i,i)), convert((i,6-i)))  # left
        pygame.draw.line(screen, (50,50,50), convert((6-i,i)), convert((6-i,6-i)))  # right
        pygame.draw.line(screen, (50,50,50), convert((i,i)), convert((6-i,i)))  # top
        pygame.draw.line(screen, (50,50,50), convert((i,6-i)), convert((6-i,6-i)))  # bottom
    pygame.draw.line(screen, (50, 50, 50), convert((0,3)), convert((2,3)))
    pygame.draw.line(screen, (50, 50, 50), convert((6,3)), convert((4,3)))
    pygame.draw.line(screen, (50, 50, 50), convert((3,0)), convert((3,2)))
    pygame.draw.line(screen, (50, 50, 50), convert((3,6)), convert((3,4)))
    # FIELDS
    for i, val in enumerate(board):
        if val == 0:
            pygame.draw.circle(screen, (60, 60, 60), convert(mills.COORDS[i]), 5)
        else:
            pygame.draw.circle(screen, (0,0,0) if val > 0 else (255,255,255), convert(mills.COORDS[i]), 30)
        screen.blit(myfont.render(str(i), 1, (70, 70, 70)), convert(mills.COORDS[i]))
    # NODES
    for i, val in enumerate(SPG.NODES):
        pygame.draw.circle(screen, (100, 100, 0), convert(val), 5)
        x, y = convert(val)
        x -= 20
        y -= 20
        screen.blit(myfont.render(str(i), 1, (100, 100, 0)), (x,y))
    # CONNECTIONS
    for i, val in enumerate(SPG.CONNECTIONS):
        for i2 in val:
            pygame.draw.line(screen, (100, 100, 0), convert(SPG.NODES[i]), convert(SPG.NODES[i2]))
    # ACCESS_POINTS
    for i, val in enumerate(SPG.ACCESS_POINTS):
        for i2 in val:
            pygame.draw.line(screen, (100, 0, 100), convert(mills.COORDS[i]), convert(SPG.NODES[i2]))
    # TEXT_BOX
    screen.blit(myfont.render(text_box, 1, (255, 255, 0)), convert((0.5, 6.1)))
    # PATH
    points = []
    for p in live_path:
        points.append(convert(p))
    if len(points) > 1:
        pygame.draw.lines(screen, (255,0,0), False, points)
    pygame.draw.circle(screen, (255,0,0), points[-1], 5)
    # UPDATE
    pygame.display.flip()

def dist(c1, c2):
    return math.sqrt((c1[0] - c2[0])**2 + (c1[1] - c2[1])**2)

def get_input(text):
    global text_box, board
    text_box = text
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                _pos = event.pos
                for i, val in enumerate(mills.COORDS):
                    if dist(convert(val), _pos) < 30:
                        return i
                return 0
        draw()

try:
    # PLAYER MOVE
    while True:
        if mills.pieces_player > 0:
            board[mills.resolve_base(-1, -mills.COLOR_AI)] = 0
        else:
            board[get_input("Start: ")] = 0
        _dest = get_input("Dest: ")
        board[_dest] = -mills.COLOR_AI
        if ai.isInMill(board, _dest):
            board[get_input("Take: ")] = 0

        mills.pieces_player = max(0, mills.pieces_player-1)
        text_box = "Thinking..."
        draw()

        # AI RESPONSE
        trimmed_board = [board[i] for i in range(24)]
        new_trimmed_board, moves = ai.calcMove(trimmed_board, mills.COLOR_AI, mills.pieces_ai, mills.pieces_player)
        # SHOW EXECUTION PATH
        for move in moves:
            start = move[0]
            dest = move[1]
            print('move: ', move[0], 'to', move[1])

            # resolve coords of start and dest & color of piece
            c1, color = mills.resolve(start, board, mills.COLOR_AI)  # can only move pieces out of own base
            c2, _ = mills.resolve(dest, board, mills.COLOR_AI)  # can only put pieces in opponents base

            # move piece from start to dest
            if start == -1 or mills.count(board, mills.COLOR_AI) <= 3 or dest == -1:
                board[mills.resolve_base(start, mills.COLOR_AI)] = 0
                path = mills.getShortSafePath(board, mills.resolve_base(start, mills.COLOR_AI), mills.resolve_base(dest, mills.COLOR_AI))
            else:
                path = [c1, c2]
            for pos in path:
                live_path.append(pos)
                time.sleep(0.5)
                draw()
            # WAIT
            board = [new_trimmed_board[i] if i < 24 else val for i, val in enumerate(board)]
            get_input("Click to continue...")
            # CLEAR PATH
            tmp = live_path[-1]
            live_path = [tmp]
        mills.pieces_ai = max(0, mills.pieces_ai-1)
        # RESET MOTORS
        live_path.append((0,0))
        live_path.append(RESET_POS)
        draw()
        time.sleep(0.5)
        # CLEAR PATH
        tmp = live_path[-1]
        live_path = [tmp]
        draw()
except KeyboardInterrupt:
    print('Interrupted!')
    pygame.quit()
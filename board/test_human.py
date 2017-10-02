#!/usr/bin/env python
import mills_old
import numpy as np
import pygame
game = mills_old.GameState()
done = False
try:
    skip_player = True
    while not done:
        try:
            print()
            print('--------- YOUR TURN ---------')
            if game.player_num_pieces > 0:
                print('you still have %d pieces to set down freely' % game.player_num_pieces)
            print('select origin (will only matter, if applicable)')
            start = mills_old.blockGetClickIndex()
            print('start = %d; select destination' % start)
            dest = mills_old.blockGetClickIndex()
            print('dest = %d; select piece to take (will only matter, if applicable)' % dest)
            take = mills_old.blockGetClickIndex()
            print('take = %d' % take)
            
            x = np.ones(24)
            x[take] = 1.5
            x[start] = 0
            x[dest] = 2
            
            print()
            print('--------- AI TURN ---------')
            _,_,done = game.frame_step(x, skip_player=skip_player)
            skip_player = False
        except IndexError:
            print('invalid click registred, try again')
except KeyboardInterrupt:
    print('test_human.py received interrupt')
    pygame.quit()
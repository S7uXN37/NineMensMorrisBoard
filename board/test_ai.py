#!/usr/bin/env python
import mills_old
import numpy as np
import pygame

game = mills_old.GameState()
try:
    for i in range(10):
        with open('log.csv', 'a') as f: # add breaks into log file to differentiate runs
            f.write('\n\n')
        done = False
        
        while not done:
            x = np.random.rand(24)
            _,_,done = game.frame_step(x)
    pygame.quit()
except KeyboardInterrupt:
    print('test_ai.py received interrupt')
    pygame.quit()

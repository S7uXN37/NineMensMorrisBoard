import morris
import numpy as np
import pygame
x = np.random.rand(24)
game = morris.GameState()
done = False
while not done:
    _,_,done = game.frame_step(x)
pygame.quit()
#!/usr/bin/env python
import motors
import input
import magnet
import time.sleep from time

board = [0]*24

while True:
	print('reading...')
	new_board = input.readBoard()
	if not board == new_board:
		print('found changes')
		desired_board = ai.calcMove(...)
		for i in range(0,24):
			if not new_board[i] == desired_board[i]:
				#Move magnet, change board
				print('found change at i=%i, resolving...' % i)
	else:
		time.sleep(2)

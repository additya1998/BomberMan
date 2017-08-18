from config import *
from board import Board
from bomber import Bomber
from threading import Timer
from random import randint
import time, getch, sys
import os
import termios
from person import *

class Enemy(Person):
	def __init__(self, X, Y, health, speed):
		Person.__init__(self, X, Y)
		self.health = health
		self.speed = speed

	def move(self, board):

		(X, Y) = (self.X, self.Y)
		arr = []

		if board.isEmpty(X - OBJECT_HEIGHT, Y):
			arr.append((-OBJECT_HEIGHT, 0))

		if board.isEmpty(X + OBJECT_HEIGHT, Y):
			arr.append((OBJECT_HEIGHT, 0))
		
		if board.isEmpty(X, Y - OBJECT_WIDTH):
			arr.append((0, -OBJECT_WIDTH))
		
		if board.isEmpty(X, Y + OBJECT_WIDTH):
			arr.append((0, OBJECT_WIDTH))

		if len(arr) == 0:
			pass
		else:
			idx = arr[randint(0, len(arr) - 1)]
			(x, y) = idx
			self.X = self.X + x
			self.Y = self.Y + y


# class Enemies:
# 	def __init__(self):
# 		allEnemies = []
# 		for i in range(0, ENEMEIES):
# 			newEnemy = Enemy()
# 			newEnemy.setPosition(board)
# 			allEnemies.append(newEnemy)
# 		self.allEnemies = allEnemies

# 	def move(self, board):
# 		for i in range(0, len(self.allEnemies)):
# 			arr = []
# 			X = self.allEnemies[i].X
# 			Y = self.allEnemies[i].Y
# 			if board.isEmpty(X - 2, Y):
# 				arr.append((-2, 0))
# 			if board.isEmpty(X, Y + 4):
# 				arr.append((0, 4))
# 			if board.isEmpty(X + 2, Y):
# 				arr.append((2, 0))
# 			if board.isEmpty(X, Y - 4):
# 				arr.append((0, -4))
			
# 			if len(arr) == 0:
# 				continue
# 			else:
# 				idx = randint(0, len(arr) - 1)
# 				board.vacate(X, Y)
# 				(x, y) = arr[idx]
# 				board.setEnemy(X + x, Y + y, 'E')
# 				self.allEnemies[i].X = X + x
# 				self.allEnemies[i].Y = Y + y

# board = Board(BOARD_HEIGHT, BOARD_WIDTH, COUNT_BRICKS)
# board.initialise()

# listOfEnemies = enemies()
# listOfEnemies.move(board)

# bomber = Bomber()
# board.show()

# # while True:
# # 	x = int(input())
# # 	listOfEnemies.move(board)
# # 	bomber.move(board, x)
# # 	board.show()


# # old_settings=None

# # def init_anykey():
# # 	global old_settings
# # 	old_settings = termios.tcgetattr(sys.stdin)
# # 	new_settings = termios.tcgetattr(sys.stdin)
# # 	new_settings[3] = new_settings[3] & ~(termios.ECHO | termios.ICANON) # lflags
# # 	new_settings[6][termios.VMIN] = 0  # cc
# # 	new_settings[6][termios.VTIME] = 0 # cc
# # 	termios.tcsetattr(sys.stdin, termios.TCSADRAIN, new_settings)

# # # @atexit.register
# # def term_anykey():
# # 	global old_settings
# # 	if old_settings:
# # 		termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

# # def anykey():
# # 	ch_set = []
# # 	ch = os.read(sys.stdin.fileno(), 1)
# # 	while ch != None and len(ch) > 0:
# # 		ch_set.append( ord(ch[0]) )
# # 		ch = os.read(sys.stdin.fileno(), 1)
# # 	return ch_set;

# # init_anykey()
# # while True:
# # 	key = str(anykey())
# # 	if key != None:
# # 		print(key)
# # 	else:
# # 		time.sleep(100)


# import sys
# import select

# def something(line):
# 	print('read input:', line, end='')

# def something_else():
# 	print('no input')

# # If there's input ready, do something, else do something
# # else. Note timeout is zero so select won't block at all.
# while sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
# 	line = sys.stdin.readline()
# 	if line:
# 		something(line)
# 	else: 
# 		something_else()

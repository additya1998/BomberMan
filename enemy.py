from config import *
from board import Board
from bomber import Bomber
from threading import Timer
from random import randint
import time, getch, sys
from os import system


class enemy:
	def __init__(self):
		self.X = 0
		self.Y = 0
		self.health = 0
		self.speed = 0
		self.alive = 1


	def setPosition(self, board):
		(self.X, self.Y) = board.getRandomEmpty()
		board.setEnemy(self.X, self.Y, 'E')

class enemies:
	def __init__(self):
		allEnemies = []
		for i in range(0, ENEMEIES):
			newEnemy = enemy()
			newEnemy.setPosition(board)
			allEnemies.append(newEnemy)
		self.allEnemies = allEnemies

	def move(self, board):
		for i in range(0, len(self.allEnemies)):
			arr = []
			X = self.allEnemies[i].X
			Y = self.allEnemies[i].Y
			if board.isEmpty(X - 2, Y):
				arr.append((-2, 0))
			if board.isEmpty(X, Y + 4):
				arr.append((0, 4))
			if board.isEmpty(X + 2, Y):
				arr.append((2, 0))
			if board.isEmpty(X, Y - 4):
				arr.append((0, -4))
			
			if len(arr) == 0:
				continue
			else:
				idx = randint(0, len(arr) - 1)
				board.vacate(X, Y)
				(x, y) = arr[idx]
				board.setEnemy(X + x, Y + y, 'E')
				self.allEnemies[i].X = X + x
				self.allEnemies[i].Y = Y + y

board = Board(BOARD_HEIGHT, BOARD_WIDTH, COUNT_BRICKS)
board.initialise()

listOfEnemies = enemies()
listOfEnemies.move(board)

bomber = Bomber()
board.show()

while True:
	x = int(input())
	listOfEnemies.move(board)
	bomber.move(board, x)
	board.show()
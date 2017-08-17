from config import BOARD_WIDTH, BOARD_HEIGHT, OBJECT_WIDTH, OBJECT_HEIGHT
from board import Board
from threading import Timer
from random import randint
import time
from os import system

class enemy:
	def __init__(self):
		self.X = 0
		self.Y = 0
		self.health = 1
		self.fire = 1

	def setPosition(self, board):
		(self.X, self.Y) = board.getRandomEmpty()
		board.setEnemy(self.X, self.Y)

def show():
	for i in range(0, len(enemies)):
		arr = []
		X = enemies[i].X
		Y = enemies[i].Y
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
			board.setEnemy(X + x, Y + y)
			enemies[i].X = X + x
			enemies[i].Y = Y + y
	board.show()

enemies = []
board = Board(BOARD_HEIGHT, BOARD_WIDTH)
board.initialise()

for i in range(0, 10):
	newEnemy = enemy()
	newEnemy.setPosition(board)
	enemies.append(newEnemy)
	# print(type(newEnemy))

# print(type(enemies[0]))

for i in range(0, 10):
	system("tput reset")
	show()
	time.sleep(2)


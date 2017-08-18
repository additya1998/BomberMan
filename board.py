from random import randint
from config import *
from os import system

class Board:

	def __init__(self, BOARD_HEIGHT, BOARD_WIDTH):
		self.board = [[' ' for j in range(0, BOARD_WIDTH)] for i in range(0, BOARD_HEIGHT)]
		self.BOARD_HEIGHT = BOARD_HEIGHT
		self.BOARD_WIDTH = BOARD_WIDTH

	def reset(self, bomber, enemies = [], bricks = []):
		self.board = [[' ' for j in range(0, BOARD_WIDTH)] for i in range(0, BOARD_HEIGHT)]
		self.setWalls()
		for enemy in enemies:
			for i in range(OBJECT_HEIGHT):
				for j in range(OBJECT_WIDTH):
					if enemy.health == 1:
						self.board[enemy.X + i][enemy.Y + j] = 'E'
					else:
						self.board[enemy.X + i][enemy.Y + j] = 'R'

		for brick in bricks:
			if brick.isDestroyed == 0:
				for i in range(OBJECT_HEIGHT):
					for j in range(OBJECT_WIDTH):
						self.board[brick.X + i][brick.Y + j] = '/'


		for i in range(OBJECT_HEIGHT):
			for j in range(OBJECT_WIDTH):
				self.board[bomber.X + i][bomber.Y + j] = 'B'



	def getRandomEmpty(self):
		arr = []
		for i in range(0, self.BOARD_HEIGHT, 4):
			for j in range(0, self.BOARD_WIDTH - 2, 4):
				if self.isEmpty(i, j):
					arr.append((i, j))
		return arr[randint(0, len(arr) - 1)]

	def setWalls(self):
		for i in range(0, 2):
			for j in range(0, self.BOARD_WIDTH):
				self.board[i][j] = 'X'
				self.board[self.BOARD_HEIGHT - i - 1][j] = 'X'

		for i in range(0, self.BOARD_HEIGHT, 4):
			for j in range(0, self.BOARD_WIDTH, 8):
				self.board[i][j] = self.board[i][j + 1] = self.board[i][j + 2] = self.board[i][j + 3] = 'X'
				self.board[i + 1][j] = self.board[i + 1][j + 1] = self.board[i + 1][j + 2] = self.board[i + 1][j + 3] = 'X'

		for i in range(0, self.BOARD_HEIGHT):
			self.board[i][0] = self.board[i][1] = self.board[i][2] = self.board[i][3] = 'X'
			self.board[i][self.BOARD_WIDTH - 1] = self.board[i][self.BOARD_WIDTH - 2] = self.board[i][self.BOARD_WIDTH - 3] = self.board[i][self.BOARD_WIDTH - 4] = 'X'

	# def placeBomber(self, bomber):
	# 	for i in range(OBJECT_HEIGHT):
	# 		for j in range(OBJECT_WIDTH):
	# 			self.board[bomber.X + i][bomber.Y + j] = 'B'

	# def placeEnemy(self, enemy):
	# 	if self.board[enemy.X][enemy.Y] != 'B':
	# 		for i in range(OBJECT_HEIGHT):
	# 			for j in range(OBJECT_WIDTH):
	# 				# if self.board[ene]
	# 				if enemy.health == 1:
	# 					self.board[enemy.X + i][enemy.Y + j] = 'E'
	# 				else:
	# 					self.board[enemy.X + i][enemy.Y + j] = 'R'

	# def placeBrick(self, brick):
	# 	for i in range(OBJECT_HEIGHT):
	# 		for j in range(OBJECT_WIDTH):
	# 			self.board[brick.X + i][brick.Y + j] = '/'


	# def initialise(self):
	# 	self.setWalls();
	# 	self.setBricks();

	def show(self):
		system("tput reset")
		for i in range(0, self.BOARD_HEIGHT):
			s = ""
			for j in range(0, self.BOARD_WIDTH):
				x = str(self.board[i][j])
				if x == 'B':
					s = s + BLUE + x + END
				elif x == 'X':
					s = s + RED + x + END
				elif x == 'E':
					s = s + GREEN + x + END
				elif x == 'R':
					s = s + MAGENTA + 'E' + END
				elif x == 'B':
					s = s + YELLOW + x + END
				elif x == '/':
					s = s + BROWN + x + END
				else:
					s = s + x
			print(s)

	def isEmpty(self, X, Y):
		if X < 0 or Y < 0:
			return 0
		valid = 1
		for i in range(OBJECT_HEIGHT):
			for j in range(OBJECT_WIDTH):
				if X + i >= self.BOARD_HEIGHT:
					return 0
				elif Y + j >= self.BOARD_WIDTH:
					return 0;
				elif self.board[X + i][Y + j] == 'X' or self.board[X +i][Y + j] == '/':
					return 0
		return 1

	# def vacate(self, X, Y):
	# 	for i in range(OBJECT_HEIGHT):
	# 		for j in range(OBJECT_WIDTH):
	# 			self.board[X + i][Y + j] = ' '


	# def setEnemy(self, X, Y, character):
	# 	for i in range(0, 2):
	# 		for j in range(0, 4):
	# 			self.board[X + i][Y + j] = character
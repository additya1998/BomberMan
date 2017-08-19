from random import randint
from config import *
from os import system

class Board:

	def __init__(self, BOARD_HEIGHT, BOARD_WIDTH):
		self.board = [[' ' for j in range(0, BOARD_WIDTH)] for i in range(0, BOARD_HEIGHT)]
		self.BOARD_HEIGHT = BOARD_HEIGHT
		self.BOARD_WIDTH = BOARD_WIDTH

	def isValid(self, X, Y):
		if X < 0 or Y < 0:
			return 0
		if X + OBJECT_HEIGHT >= self.BOARD_HEIGHT or Y + OBJECT_WIDTH >= self.BOARD_WIDTH:
			return 0
		return 1

	def reset(self, bomber, enemies, bricks, bomb):
		self.board = [[' ' for j in range(0, BOARD_WIDTH)] for i in range(0, BOARD_HEIGHT)]
		self.setWalls()

		if bomb:
			if bomb.active and bomb.showBlast == 0:
				for i in range(OBJECT_HEIGHT):
					for j in range(OBJECT_WIDTH):
						self.board[bomb.X + i][bomb.Y + j] = bomb.timeLeft


		for enemy in enemies:
			for i in range(OBJECT_HEIGHT):
				for j in range(OBJECT_WIDTH):
					if enemy.health == 1:
						self.board[enemy.X + i][enemy.Y + j] = 'E'
					elif enemy.health == 2:
						self.board[enemy.X + i][enemy.Y + j] = 'R'

		for brick in bricks:
			if brick.isDestroyed == 0:
				# print(brick.X, brick.Y)
				for i in range(OBJECT_HEIGHT):
					for j in range(OBJECT_WIDTH):
						self.board[brick.X + i][brick.Y + j] = '/'
			else:
				if brick.isExit:
					for i in range(OBJECT_HEIGHT):
						for j in range(OBJECT_WIDTH):
							self.board[brick.X + i][brick.Y + j] = 'D'


		for i in range(OBJECT_HEIGHT):
			for j in range(OBJECT_WIDTH):
				self.board[bomber.X + i][bomber.Y + j] = 'B'

		if bomb:
			if bomb.active == 1 and bomb.showBlast == 1:

				# Horizontal
				left = bomb.length
				right = bomb.length

				# print(bomb.X, bomb.Y)
				# print(bomb.X, bomb.Y - OBJECT_HEIGHT)
				# print(self.board[bomb.X][bomb.Y - OBJECT_HEIGHT])

				for i in range(0, bomb.length + 1):
					if self.isValid(bomb.X, bomb.Y - OBJECT_WIDTH * i) == 0:
						left = i - 1
						break
					else:	
						if self.board[bomb.X][bomb.Y - OBJECT_WIDTH * i] == 'X':
							left = i - 1
							break
						elif self.board[bomb.X][bomb.Y - OBJECT_WIDTH * i] == '/':
							left = i
							break 
					
				for i in range(0, bomb.length + 1):
					if self.isValid(bomb.X, bomb.Y + OBJECT_WIDTH * i) == 0:
						right = i - 1
						break
					else:	
						if self.board[bomb.X][bomb.Y + OBJECT_WIDTH * i] == 'X':
							right = i - 1
							break
						elif self.board[bomb.X][bomb.Y + OBJECT_WIDTH * i] == '/':
							right = i
							break 
					
				up = bomb.length
				down = bomb.length
				for i in range(0, bomb.length + 1):
					if self.isValid(bomb.X - OBJECT_HEIGHT * i, bomb.Y) == 0:
						up = i - 1
						break
					else:	
						if self.board[bomb.X - OBJECT_HEIGHT * i][bomb.Y] == 'X':
							up = i - 1
							break
						elif self.board[bomb.X - OBJECT_HEIGHT * i][bomb.Y] == '/':
							up = i
							break
					
				for i in range(0, bomb.length + 1):
					if self.isValid(bomb.X + OBJECT_HEIGHT * i, bomb.Y) == 0:
						down = i - 1
						break
					else:	
						if self.board[bomb.X + OBJECT_HEIGHT * i][bomb.Y] == 'X':
							down = i - 1
							break
						elif self.board[bomb.X + OBJECT_HEIGHT * i][bomb.Y] == '/':
							down = i
							break

				# Horizontal
				for i in range(bomb.Y - OBJECT_WIDTH * left, bomb.Y + OBJECT_WIDTH * (right + 1)):
					for j in range(bomb.X, bomb.X + OBJECT_HEIGHT):
						if self.isValid(j, i) and self.board[j][i] != 'X':
							self.board[j][i] = 'O'

				# Vertical
				for i in range(bomb.X - OBJECT_HEIGHT * up, bomb.X + OBJECT_HEIGHT * (down + 1)):
					for j in range(bomb.Y, bomb.Y + OBJECT_WIDTH):
						if self.isValid(i, j) and self.board[i][j] != 'X':
							self.board[i][j] = 'O'


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

	def show(self):
		system("tput reset")
		for i in range(0, self.BOARD_HEIGHT):
			s = ""
			for j in range(0, self.BOARD_WIDTH):
				x = str(self.board[i][j])
				# s = s +
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
				elif x == 'O':
					s = s + YELLOW_BACKGROUND + x + END
				else :
					s = s + x
			print(s)
		print("\n")

	def isEmpty(self, X, Y):
		if self.isValid(X, Y) == 0:
			return 0

		for i in range(OBJECT_HEIGHT):
			for j in range(OBJECT_WIDTH):
				if self.board[X + i][Y + j] == 'X' or self.board[X +i][Y + j] == '/':
					return 0
				if self.board[X + i][Y + j] == 1 or self.board[X + i][Y + j] == 2 or self.board[X + i][Y + j] == 3:
					return 0 
		return 1


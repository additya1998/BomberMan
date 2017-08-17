from random import randint

class Board:

	def __init__(self, BOARD_HEIGHT, BOARD_WIDTH):
		self.board = [[' ' for j in range(0, BOARD_WIDTH)] for i in range(0, BOARD_HEIGHT)]
		self.BOARD_HEIGHT = BOARD_HEIGHT
		self.BOARD_WIDTH = BOARD_WIDTH

	def initialise(self):
		for i in range(0, 2):
			for j in range(0, self.BOARD_WIDTH):
				self.board[i][j] = '#'
				self.board[self.BOARD_HEIGHT - i - 1][j] = '#'

		for i in range(0, self.BOARD_HEIGHT):
			self.board[i][0] = self.board[i][1] = '#'
			self.board[i][self.BOARD_WIDTH - 1] = self.board[i][self.BOARD_WIDTH - 2] = '#'

		for i in range(4, self.BOARD_HEIGHT, 4):
			for j in range(6, self.BOARD_WIDTH, 8):
				self.board[i][j] = self.board[i + 1][j] = '#' 
				if j + 1 < self.BOARD_WIDTH:	
					self.board[i][j + 1] = self.board[i + 1][j + 1] = '#' 
				if j + 2 < self.BOARD_WIDTH:
					self.board[i][j + 2] = self.board[i + 1][j + 2] = '#' 
				if j + 3 < self.BOARD_WIDTH:
					self.board[i][j + 3] = self.board[i + 1][j + 3] = '#' 

	def show(self):
		for i in range(0, self.BOARD_HEIGHT):
			s = ""
			for j in range(0, self.BOARD_WIDTH):
				s = s + str(self.board[i][j])
			print(s)

	def isEmpty(self, X, Y):
		if X < 0 or Y < 0:
			return 0
		valid = 1
		for i in range(0, 2):
			for j in range(0, 4):
				if X + i >= self.BOARD_HEIGHT:
					return 0
				elif Y + j >= self.BOARD_WIDTH:
					return 0;
				elif self.board[X + i][Y + j] != ' ':
					return 0
		return 1

	def vacate(self, X, Y):
		for i in range(0, 2):
			for j in range(0, 4):
				self.board[X + i][Y + j] = ' '

	def getRandomEmpty(self):
		arr = []
		for i in range(2, self.BOARD_HEIGHT, 4):
			for j in range(2, self.BOARD_WIDTH - 2, 4):
				if self.isEmpty(i, j):
					arr.append((i, j))
		return arr[randint(0, len(arr) - 1)]

	def setEnemy(self, X, Y):
		for i in range(0, 2):
			for j in range(0, 4):
				self.board[X + i][Y + j] = 'E'
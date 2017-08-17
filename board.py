from random import randint

class Board:

	def __init__(self, BOARD_HEIGHT, BOARD_WIDTH, COUNT_BRICKS):
		self.__board = [[' ' for j in range(0, BOARD_WIDTH)] for i in range(0, BOARD_HEIGHT)]
		self.__BOARD_HEIGHT = BOARD_HEIGHT
		self.__BOARD_WIDTH = BOARD_WIDTH
		self.__COUNT_BRICKS = COUNT_BRICKS
		for i in range(0, 2):
			for j in range(0, 4):
				self.__board[2 + i][2 + j] = 'B'

	def getRandomEmpty(self):
		arr = []
		for i in range(2, self.__BOARD_HEIGHT, 4):
			for j in range(2, self.__BOARD_WIDTH - 2, 4):
				if self.isEmpty(i, j):
					arr.append((i, j))
		return arr[randint(0, len(arr) - 1)]

	def setWalls(self):
		for i in range(0, 2):
			for j in range(0, self.__BOARD_WIDTH):
				self.__board[i][j] = 'X'
				self.__board[self.__BOARD_HEIGHT - i - 1][j] = 'X'

		for i in range(0, self.__BOARD_HEIGHT):
			self.__board[i][0] = self.__board[i][1] = 'X'
			self.__board[i][self.__BOARD_WIDTH - 1] = self.__board[i][self.__BOARD_WIDTH - 2] = 'X'

		for i in range(4, self.__BOARD_HEIGHT, 4):
			for j in range(6, self.__BOARD_WIDTH, 8):
				self.__board[i][j] = self.__board[i + 1][j] = 'X' 
				if j + 1 < self.__BOARD_WIDTH:	
					self.__board[i][j + 1] = self.__board[i + 1][j + 1] = 'X' 
				if j + 2 < self.__BOARD_WIDTH:
					self.__board[i][j + 2] = self.__board[i + 1][j + 2] = 'X' 
				if j + 3 < self.__BOARD_WIDTH:
					self.__board[i][j + 3] = self.__board[i + 1][j + 3] = 'X' 

	def setBricks(self):
		for i in range(0, self.__COUNT_BRICKS):
			(X, Y) = self.getRandomEmpty()
			for j in range(0, 2):
				for k in range(0, 4):
					self.__board[X + j][Y + k] = '/'

	def initialise(self):
		self.setWalls();
		self.setBricks();

	def show(self):
		for i in range(0, self.__BOARD_HEIGHT):
			s = ""
			for j in range(0, self.__BOARD_WIDTH):
				s = s + str(self.__board[i][j])
			print(s)

	def isEmpty(self, X, Y):
		if X < 0 or Y < 0:
			return 0
		valid = 1
		for i in range(0, 2):
			for j in range(0, 4):
				if X + i >= self.__BOARD_HEIGHT:
					return 0
				elif Y + j >= self.__BOARD_WIDTH:
					return 0;
				elif self.__board[X + i][Y + j] != ' ':
					return 0
		return 1

	def vacate(self, X, Y):
		for i in range(0, 2):
			for j in range(0, 4):
				self.__board[X + i][Y + j] = ' '


	def setEnemy(self, X, Y):
		for i in range(0, 2):
			for j in range(0, 4):
				self.__board[X + i][Y + j] = 'E'
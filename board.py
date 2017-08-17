from config import BOARD_WIDTH, BOARD_HEIGHT, OBJECT_WIDTH, OBJECT_HEIGHT

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


board = Board(BOARD_HEIGHT, BOARD_WIDTH)
board.initialise()
board.show()

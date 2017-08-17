class Bomber:
	
	def __init__(self):
		self.__X = 2
		self.__Y = 2

	def move(self, board, direction):
		#UP
		if direction == 1:
			if board.isEmpty(self.__X - 2, self.__Y):
				board.vacate(self.__X, self.__Y)
				board.setEnemy(self.__X - 2, self.__Y, 'B')
				self.__X = self.__X - 2

		elif direction == 2:
			if board.isEmpty(self.__X, self.__Y + 4):
				board.vacate(self.__X, self.__Y)
				board.setEnemy(self.__X, self.__Y + 4, 'B')
				self.__Y = self.__Y + 4

		elif direction == 3:
			if board.isEmpty(self.__X + 2, self.__Y):
				board.vacate(self.__X, self.__Y)
				board.setEnemy(self.__X + 2, self.__Y, 'B')
				self.__X = self.__X + 2
				
		elif direction == 4:
			if board.isEmpty(self.__X, self.__Y - 4):

				board.vacate(self.__X, self.__Y)
				board.setEnemy(self.__X, self.__Y - 4, 'B')
				self.__Y = self.__Y - 4

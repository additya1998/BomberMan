from person import *
from config import *

class Bomber(Person):
	
	def __init__(self, X, Y):
		Person.__init__(self, X, Y)
		self.health = 1
		self.speed = 0

	def moveBomber(self, direction, board):
		(X, Y) = (self.X, self.Y)
		if direction == 'w' or direction == 'W':
			if board.isEmpty(X - OBJECT_HEIGHT, Y):
				self.X = self.X - OBJECT_HEIGHT

		elif direction == 'a' or direction == 'A':
			if board.isEmpty(X, Y - OBJECT_WIDTH):
				self.Y = self.Y - OBJECT_WIDTH

		elif direction == 's' or direction == 'S':
			if board.isEmpty(X + OBJECT_HEIGHT, Y):
				self.X = self.X + OBJECT_HEIGHT

		elif direction == 'd' or direction == 'D':
			if board.isEmpty(X, Y + OBJECT_WIDTH):
				self.Y = self.Y + OBJECT_WIDTH
		
		elif direction == 'b' or direction == 'B':
			pass

	# def move(self, board, direction):
	# 	#UP
	# 	if direction == 1:
	# 		if board.isEmpty(self.__X - 2, self.__Y):
	# 			board.vacate(self.__X, self.__Y)
	# 			board.setEnemy(self.__X - 2, self.__Y, 'B')
	# 			self.__X = self.__X - 2

	# 	elif direction == 2:
	# 		if board.isEmpty(self.__X, self.__Y + 4):
	# 			board.vacate(self.__X, self.__Y)
	# 			board.setEnemy(self.__X, self.__Y + 4, 'B')
	# 			self.__Y = self.__Y + 4

	# 	elif direction == 3:
	# 		if board.isEmpty(self.__X + 2, self.__Y):
	# 			board.vacate(self.__X, self.__Y)
	# 			board.setEnemy(self.__X + 2, self.__Y, 'B')
	# 			self.__X = self.__X + 2
				
	# 	elif direction == 4:
	# 		if board.isEmpty(self.__X, self.__Y - 4):

	# 			board.vacate(self.__X, self.__Y)
	# 			board.setEnemy(self.__X, self.__Y - 4, 'B')
	# 			self.__Y = self.__Y - 4

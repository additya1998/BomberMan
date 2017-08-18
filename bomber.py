from person import *
from config import *

class Bomber(Person):
	
	def __init__(self, X, Y):
		Person.__init__(self, X, Y, health = 1)
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
		

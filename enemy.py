from config import *
from board import Board
from random import randint
from person import *

class Enemy(Person):
	def __init__(self, X, Y, speed, health, prevTime):
		Person.__init__(self, X, Y, health)
		self.speed = speed
		self.prevTime = prevTime

	def move(self, board):

		(X, Y) = (self.getX(), self.getY())
		arr = []

		if board.isEmpty(X - OBJECT_HEIGHT, Y):
			arr.append((-OBJECT_HEIGHT, 0))

		if board.isEmpty(X + OBJECT_HEIGHT, Y):
			arr.append((OBJECT_HEIGHT, 0))
		
		if board.isEmpty(X, Y - OBJECT_WIDTH):
			arr.append((0, -OBJECT_WIDTH))
		
		if board.isEmpty(X, Y + OBJECT_WIDTH):
			arr.append((0, OBJECT_WIDTH))

		if len(arr) == 0:
			pass
		else:
			idx = arr[randint(0, len(arr) - 1)]
			(x, y) = idx
			(X, Y) = (self.getX(), self.getY())
			self.setX(X + x)
			self.setY(Y + y)
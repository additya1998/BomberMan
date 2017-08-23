from position import *

class Person(Position):
	def __init__(self, X, Y, health):
		Position.__init__(self, X, Y)
		self.__health = health

	def getHealth(self):
		return self.__health

	def setHealth(self, value):
		self.__health = value

	def move(self, X, Y):
		self.setX(X); 
		self.setY(Y);
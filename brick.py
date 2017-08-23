from position import *

class Brick(Position):
	def __init__(self, X, Y, isExit = 0, isDestroyed = 0): 
		Position.__init__(self, X, Y)
		self.__isExit = isExit
		self.__isDestroyed = isDestroyed

	def checkExit(self):
		return self.__isExit

	def checkDestroyed(self):
		return self.__isDestroyed

	def setDestroyed(self):
		self.__isDestroyed = 1

	def setExit(self):
		self.__isExit = 1

from time import time
from config import POWER_UP_LENGTH
from position import*

class PowerUp(Position):
	def __init__(self, X, Y, previousTime):
		Position.__init__(self, X, Y)
		self.__previousTime = previousTime
		self.__active = 1

	def update(self):
		current_time = time()
		if current_time - self.__previousTime > POWER_UP_LENGTH:
			self.__active = 0

	def isActive(self):
		return self.__active

	def setInActive(self):
		self.__active = 0
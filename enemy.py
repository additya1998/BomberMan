from config import *
from board import Board
from random import randint
from person import *

class Enemy(Person):
	def __init__(self, X, Y, speed, health, prevTime):
		Person.__init__(self, X, Y, health)
		self.__speed = speed
		self.__prevTime = prevTime

	def getPrevTime(self):
		return self.__prevTime

	def getSpeed(self):
		return self.__speed

	def setPrevTime(self, time):
		self.__prevTime = time

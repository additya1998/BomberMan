from time import time
from config import *

class Bomb:
	def __init__(self, X, Y, timeLeft, active, previousTime, length = 3):
		self.X = X
		self.Y = Y
		self.timeLeft = timeLeft
		self.active = active
		self.previousTime = previousTime
		self.length = length
		self.showBlast = 0
		self.blastTime = 0

	def plantBomb(self, X, Y):
		if self.active == 0:
			self.X = X
			self.Y = Y
			self.timeLeft = 3
			self.active = 1
			self.previousTime = time()
			self.showBlast = 0
			self.blastTime = 0

	def checkBlast(self):
		if self.active:
			if self.showBlast == 0:
				current_time = time()
				seconds = current_time - self.previousTime
				if seconds > 1:
					self.previousTime = current_time
					self.timeLeft = self.timeLeft - 1
					if self.timeLeft == 0:
						self.showBlast = 1
						self.blastTime = current_time
					else:
						self.showBlast = 0

		if self.showBlast:
			current_time = time()
			if current_time - self.blastTime > BOMB_TIME_LENGTH:
				self.timeLeft = 0
				self.active = 0
				self.previousTime = 0
				self.showBlast = 0
				self.blastTime = 0


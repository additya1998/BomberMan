from time import time
class Bomb:
	def __init__(self, X, Y, timeLeft, active, previousTime, length = 100):
		self.X = X
		self.Y = Y
		self.timeLeft = timeLeft
		self.active = active
		self.previousTime = previousTime
		self.length = length

	def plantBomb(self, X, Y):
		if self.active == 0:
			self.X = X
			self.Y = Y
			self.timeLeft = 3
			self.active = 1
			self.previousTime = time()

	def updateTime(self):
		if self.active:
			currentTime = time()
			if currentTime - self.previousTime > 1:
				self.previousTime = currentTime
				self.timeLeft = self.timeLeft - 1
				if self.timeLeft == 0:
					return 1
				return 0
		


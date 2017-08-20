from time import time
from config import POWER_UP_LENGTH

class PowerUp:
	def __init__(self, X, Y, previousTime):
		self.X = X
		self.Y = Y
		self.previousTime = previousTime
		self.isActive = 1

	def update(self):
		current_time = time()
		if current_time - self.previousTime > POWER_UP_LENGTH:
			self.isActive = 0
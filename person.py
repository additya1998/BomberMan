class Person:
	def __init__(self, X, Y, health):
		self.X = X
		self.Y = Y
		self.health = health

	def getX(self):
		return self.X

	def getY(self):
		return self.Y

	def setX(self, value):
		self.X = value

	def setY(self, value):
		self.Y = value

	def getHealth(self):
		return self.health

	def setHealth(self, value):
		self.health = value

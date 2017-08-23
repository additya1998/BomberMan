from position import *
from time import time
from config import *

class Bomb(Position):
	def __init__(self, X, Y, timeLeft, active, previousTime, length = 1):
		Position.__init__(self, X, Y)
		self.__timeLeft = timeLeft
		self.__active = active
		self.__previousTime = previousTime
		self.__length = length
		self.__showBlast = 0
		self.__blastTime = 0

	def getTimeLeft(self):
		return self.__timeLeft

	def getLength(self):
		return self.__length

	def isActive(self):
		return self.__active

	def makeInactive(self):
		self.__active = 0

	def getShowBlast(self):
		return self.__showBlast

	def plantBomb(self, X, Y):
		if self.__active == 0:
			self.setX(X)
			self.setY(Y)
			self.__timeLeft = 3
			self.__active = 1
			self.__previousTime = time()
			self.__showBlast = 0
			self.__blastTime = 0

	def checkBlast(self):
		if self.__active:
			if self.__showBlast == 0:
				current_time = time()
				seconds = current_time - self.__previousTime
				if seconds > 1:
					self.__previousTime = current_time
					self.__timeLeft = self.__timeLeft - 1
					if self.__timeLeft == 0:
						self.__showBlast = 1
						self.__blastTime = current_time
					else:
						self.__showBlast = 0

		if self.__showBlast:
			current_time = time()
			if current_time - self.__blastTime > BOMB_TIME_LENGTH:
				self.__timeLeft = 0
				self.__active = 0
				self.__previousTime = 0
				self.__showBlast = 0
				self.__blastTime = 0

	def update(self, bomber, board, bricks, enemies, score):
		f = 1
		for i in range(self.__length + 1):
			(X, Y) = (self.getX() - i * OBJECT_HEIGHT, self.getY())
			if board.isValid(X, Y):
				if board.board[X][Y] == WALL_SYMBOL:
					f = 0
					break
				for brick in bricks:
					if (brick.getX(), brick.getY()) == (X, Y) and brick.checkDestroyed() == 0:
						brick.setDestroyed()
						score = score +  BRICK_SCORE
						f = 0
						break
				if f == 0:
					break
				for enemy in enemies:
					if (enemy.getX(), enemy.getY()) == (X, Y) and enemy.getHealth() > 0:
						enemy.setHealth(enemy.getHealth() - 1)
						if enemy.getHealth() == 0:
							score = score + ENEMY_SCORE
				if (X, Y) == (bomber.getX(), bomber.getY()):
					bomber.setHealth(bomber.getHealth() - 1)		

		# DOWN
		f = 1
		for i in range(self.__length + 1):
			(X, Y) = (self.getX() + i * OBJECT_HEIGHT, self.getY())
			if board.isValid(X, Y):
				if board.board[X][Y] == WALL_SYMBOL:
					f = 0
					break
				for brick in bricks:
					if (brick.getX(), brick.getY()) == (X, Y) and brick.checkDestroyed() == 0:
						brick.setDestroyed()
						score = score +  BRICK_SCORE
						f = 0
						break
				if f == 0:
					break
				for enemy in enemies:
					if (enemy.getX(), enemy.getY()) == (X, Y) and enemy.getHealth() > 0:
						enemy.setHealth(enemy.getHealth() - 1)
						if enemy.getHealth() == 0:
							score = score + ENEMY_SCORE
				if (X, Y) == (bomber.getX(), bomber.getY()) and bomber.getHealth() > 0:
					bomber.setHealth(bomber.getHealth() - 1)		

		# LEFT
		f = 1
		for i in range(self.__length + 1):
			(X, Y) = (self.getX(), self.getY() - i * OBJECT_WIDTH)
			if board.isValid(X, Y):
				if board.board[X][Y] == WALL_SYMBOL:
					f = 0
					break
				for brick in bricks:
					if (brick.getX(), brick.getY()) == (X, Y) and brick.checkDestroyed() == 0:
						brick.setDestroyed()
						score = score +  BRICK_SCORE
						f = 0
						break
				if f == 0:
					break
				for enemy in enemies:
					if (enemy.getX(), enemy.getY()) == (X, Y) and enemy.getHealth() > 0:
						enemy.setHealth(enemy.getHealth() - 1)
						if enemy.getHealth() == 0:
							score = score + ENEMY_SCORE
				if (X, Y) == (bomber.getX(), bomber.getY()) and bomber.getHealth() > 0:
					bomber.setHealth(bomber.getHealth() - 1)		

		# RIGHT
		f = 1
		for i in range(self.__length + 1):
			(X, Y) = (self.getX(), self.getY() + i * OBJECT_WIDTH)
			if board.isValid(X, Y):
				if board.board[X][Y] == WALL_SYMBOL:
					f = 0
					break
				for brick in bricks:
					if (brick.getX(), brick.getY()) == (X, Y) and brick.checkDestroyed() == 0:
						brick.setDestroyed()
						score = score +  BRICK_SCORE
						f = 0
						break
				if f == 0:
					break
				for enemy in enemies:
					if (enemy.getX(), enemy.getY()) == (X, Y) and enemy.getHealth() > 0:
						enemy.setHealth(enemy.getHealth() - 1)
						if enemy.getHealth() == 0:
							score = score + ENEMY_SCORE
				if (X, Y) == (bomber.getX(), bomber.getY()) and bomber.getHealth() > 0:
					bomber.setHealth(bomber.getHealth() - 1)		

		return score
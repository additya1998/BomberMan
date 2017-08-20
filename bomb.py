from time import time
from config import *

class Bomb:
	def __init__(self, X, Y, timeLeft, active, previousTime, length = 1):
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

	def updateBomb(self, bomber, board, bricks, enemies, score):
		f = 1
		for i in range(self.length + 1):
			(X, Y) = (self.X - i * OBJECT_HEIGHT, self.Y)
			if board.isValid(X, Y):
				if board.board[X][Y] == WALL_SYMBOL:
					f = 0
					break
				for brick in bricks:
					if (brick.X, brick.Y) == (X, Y) and brick.isDestroyed == 0:
						brick.isDestroyed = 1
						score = score +  BRICK_SCORE
						f = 0
						break
				if f == 0:
					break
				for enemy in enemies:
					if (enemy.getX(), enemy.getY()) == (X, Y) and enemy.getHealth() > 0:
						enemy.health = enemy.health - 1
						if enemy.health == 0:
							score = score + ENEMY_SCORE
				if (X, Y) == (bomber.getX(), bomber.getY()):
					bomber.setHealth(bomber.getHealth() - 1)		

		# DOWN
		f = 1
		for i in range(self.length + 1):
			(X, Y) = (self.X + i * OBJECT_HEIGHT, self.Y)
			if board.isValid(X, Y):
				if board.board[X][Y] == WALL_SYMBOL:
					f = 0
					break
				for brick in bricks:
					if (brick.X, brick.Y) == (X, Y) and brick.isDestroyed == 0:
						brick.isDestroyed = 1
						score = score +  BRICK_SCORE
						f = 0
						break
				if f == 0:
					break
				for enemy in enemies:
					if (enemy.getX(), enemy.getY()) == (X, Y) and enemy.getHealth() > 0:
						enemy.health = enemy.health - 1
						if enemy.health == 0:
							score = score + ENEMY_SCORE
				if (X, Y) == (bomber.getX(), bomber.getY()) and bomber.health > 0:
					bomber.setHealth(bomber.getHealth() - 1)		

		# LEFT
		f = 1
		for i in range(self.length + 1):
			(X, Y) = (self.X, self.Y - i * OBJECT_WIDTH)
			if board.isValid(X, Y):
				if board.board[X][Y] == WALL_SYMBOL:
					f = 0
					break
				for brick in bricks:
					if (brick.X, brick.Y) == (X, Y) and brick.isDestroyed == 0:
						brick.isDestroyed = 1
						score = score +  BRICK_SCORE
						f = 0
						break
				if f == 0:
					break
				for enemy in enemies:
					if (enemy.getX(), enemy.getY()) == (X, Y) and enemy.getHealth() > 0:
						enemy.health = enemy.health - 1
						if enemy.health == 0:
							score = score + ENEMY_SCORE
				if (X, Y) == (bomber.getX(), bomber.getY()) and bomber.health > 0:
					bomber.setHealth(bomber.getHealth() - 1)		

		# RIGHT
		f = 1
		for i in range(self.length + 1):
			(X, Y) = (self.X, self.Y + i * OBJECT_WIDTH)
			if board.isValid(X, Y):
				if board.board[X][Y] == WALL_SYMBOL:
					f = 0
					break
				for brick in bricks:
					if (brick.X, brick.Y) == (X, Y) and brick.isDestroyed == 0:
						brick.isDestroyed = 1
						score = score +  BRICK_SCORE
						f = 0
						break
				if f == 0:
					break
				for enemy in enemies:
					if (enemy.getX(), enemy.getY()) == (X, Y) and enemy.getHealth() > 0:
						enemy.health = enemy.health - 1
						if enemy.health == 0:
							score = score + ENEMY_SCORE
				if (X, Y) == (bomber.getX(), bomber.getY()) and bomber.health > 0:
					bomber.setHealth(bomber.getHealth() - 1)		

		return score
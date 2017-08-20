from random import randint
from config import *
from os import system
from time import sleep

class Board:

	def __init__(self, BOARD_HEIGHT, BOARD_WIDTH):
		self.board = [[' ' for j in range(BOARD_WIDTH)] for i in range(BOARD_HEIGHT)]
		self.BOARD_HEIGHT = BOARD_HEIGHT
		self.BOARD_WIDTH = BOARD_WIDTH

	def isValid(self, X, Y):
		if X < 0 or Y < 0:
			return 0
		if X + OBJECT_HEIGHT >= self.BOARD_HEIGHT or Y + OBJECT_WIDTH >= self.BOARD_WIDTH:
			return 0
		return 1

	def reset(self, bomber, enemies, bricks, bomb, powerUps):
		self.board = [[' ' for j in range(BOARD_WIDTH)] for i in range(BOARD_HEIGHT)]
		self.setWalls()

		if bomb:
			if bomb.active and bomb.showBlast == 0:
				for i in range(OBJECT_HEIGHT):
					for j in range(OBJECT_WIDTH):
						self.board[bomb.X + i][bomb.Y + j] = bomb.timeLeft

		for enemy in enemies:
			for i in range(OBJECT_HEIGHT):
				for j in range(OBJECT_WIDTH):
					(health, X, Y) = (enemy.getHealth(), enemy.getX(), enemy.getY())
					if health == 1:
						self.board[X + i][Y + j] = SINGLE_HEALTH_ENEMY_SYMBOL
					elif health == 2:
						self.board[X + i][Y + j] = DOUBLE_HEALTH_ENEMY_SYMBOL

		for brick in bricks:
			if brick.isDestroyed == 0:
				for i in range(OBJECT_HEIGHT):
					for j in range(OBJECT_WIDTH):
						self.board[brick.X + i][brick.Y + j] = BRICK_SYMBOL
			else:
				if brick.isExit:
					for i in range(OBJECT_HEIGHT):
						for j in range(OBJECT_WIDTH):
							self.board[brick.X + i][brick.Y + j] = DOOR_SYMBOL


		for i in range(OBJECT_HEIGHT):
			for j in range(OBJECT_WIDTH):
				self.board[bomber.getX() + i][bomber.getY() + j] = BOMBER_MAN_SYMBOL

		for powerUp in powerUps:
			for i in range(OBJECT_HEIGHT):
				for j in range(OBJECT_WIDTH):
					if powerUp.isActive:
						self.board[powerUp.X + i][powerUp.Y + j] = POWER_UP_SYMBOL

		if bomb:
			if bomb.showBlast == 1:

				# Horizontal
				left = bomb.length
				right = bomb.length


				for i in range(bomb.length + 1):
					if self.isValid(bomb.X, bomb.Y - OBJECT_WIDTH * i) == 0:
						left = i - 1
						break
					else:	
						if self.board[bomb.X][bomb.Y - OBJECT_WIDTH * i] == WALL_SYMBOL:
							left = i - 1
							break
						elif self.board[bomb.X][bomb.Y - OBJECT_WIDTH * i] == BRICK_SYMBOL:
							left = i
							break 
					
				for i in range(bomb.length + 1):
					if self.isValid(bomb.X, bomb.Y + OBJECT_WIDTH * i) == 0:
						right = i - 1
						break
					else:	
						if self.board[bomb.X][bomb.Y + OBJECT_WIDTH * i] == WALL_SYMBOL:
							right = i - 1
							break
						elif self.board[bomb.X][bomb.Y + OBJECT_WIDTH * i] == BRICK_SYMBOL:
							right = i
							break 
					
				up = bomb.length
				down = bomb.length
				for i in range(bomb.length + 1):
					if self.isValid(bomb.X - OBJECT_HEIGHT * i, bomb.Y) == 0:
						up = i - 1
						break
					else:	
						if self.board[bomb.X - OBJECT_HEIGHT * i][bomb.Y] == WALL_SYMBOL:
							up = i - 1
							break
						elif self.board[bomb.X - OBJECT_HEIGHT * i][bomb.Y] == BRICK_SYMBOL:
							up = i
							break
					
				for i in range(bomb.length + 1):
					if self.isValid(bomb.X + OBJECT_HEIGHT * i, bomb.Y) == 0:
						down = i - 1
						break
					else:	
						if self.board[bomb.X + OBJECT_HEIGHT * i][bomb.Y] == WALL_SYMBOL:
							down = i - 1
							break
						elif self.board[bomb.X + OBJECT_HEIGHT * i][bomb.Y] == BRICK_SYMBOL:
							down = i
							break

				# Horizontal
				for i in range(bomb.Y - OBJECT_WIDTH * left, bomb.Y + OBJECT_WIDTH * (right + 1)):
					for j in range(bomb.X, bomb.X + OBJECT_HEIGHT):
						if self.isValid(j, i) and self.board[j][i] != WALL_SYMBOL:
							self.board[j][i] = BOMB_SYMBOL

				# Vertical
				for i in range(bomb.X - OBJECT_HEIGHT * up, bomb.X + OBJECT_HEIGHT * (down + 1)):
					for j in range(bomb.Y, bomb.Y + OBJECT_WIDTH):
						if self.isValid(i, j) and self.board[i][j] != WALL_SYMBOL:
							self.board[i][j] = BOMB_SYMBOL

	def getRandomEmpty(self):
		arr = []
		for i in range(0, self.BOARD_HEIGHT, 4):
			for j in range(0, self.BOARD_WIDTH - 2, 4):
				if self.isEmpty(i, j):
					arr.append((i, j))
		return arr[randint(0, len(arr) - 1)]

	def setWalls(self):
		for i in range(0, 2):
			for j in range(0, self.BOARD_WIDTH):
				self.board[i][j] = WALL_SYMBOL
				self.board[self.BOARD_HEIGHT - i - 1][j] = WALL_SYMBOL

		for i in range(0, self.BOARD_HEIGHT, 4):
			for j in range(0, self.BOARD_WIDTH, 8):
				self.board[i][j] = self.board[i][j + 1] = self.board[i][j + 2] = self.board[i][j + 3] = WALL_SYMBOL
				self.board[i + 1][j] = self.board[i + 1][j + 1] = self.board[i + 1][j + 2] = self.board[i + 1][j + 3] = WALL_SYMBOL

		for i in range(0, self.BOARD_HEIGHT):
			self.board[i][0] = self.board[i][1] = self.board[i][2] = self.board[i][3] = WALL_SYMBOL
			self.board[i][self.BOARD_WIDTH - 1] = self.board[i][self.BOARD_WIDTH - 2] = self.board[i][self.BOARD_WIDTH - 3] = self.board[i][self.BOARD_WIDTH - 4] = WALL_SYMBOL

	def show(self, level, lives, timeLeft, score):
		system("tput reset")
		for i in range(0, self.BOARD_HEIGHT):
			s = ""
			for j in range(0, self.BOARD_WIDTH):
				x = str(self.board[i][j])
				# s = s +
				if x == BOMBER_MAN_SYMBOL:
					s = s + BLUE + x + END
				elif x == WALL_SYMBOL:
					s = s + RED + x + END
				elif x == SINGLE_HEALTH_ENEMY_SYMBOL:
					s = s + GREEN + x + END
				elif x == DOUBLE_HEALTH_ENEMY_SYMBOL:
					s = s + MAGENTA + SINGLE_HEALTH_ENEMY_SYMBOL + END
				elif x == BOMBER_MAN_SYMBOL:
					s = s + YELLOW + x + END
				elif x == BRICK_SYMBOL:
					s = s + BROWN + x + END
				elif x == BOMB_SYMBOL:
					s = s + YELLOW_BACKGROUND + x + END
				else :
					s = s + x
			print(s)
		print("\n")
		print("CURRENT LEVEL : " + str(level))
		print("LIVES LEFT : " + str(lives))
		print("TIME LEFT : " + str(timeLeft))
		print("SCORE : " + str(score))

	def isEmpty(self, X, Y):
		if self.isValid(X, Y) == 0:
			return 0

		for i in range(OBJECT_HEIGHT):
			for j in range(OBJECT_WIDTH):
				if self.board[X + i][Y + j] == WALL_SYMBOL or self.board[X +i][Y + j] == BRICK_SYMBOL:
					return 0
				if self.board[X + i][Y + j] == 1 or self.board[X + i][Y + j] == 2 or self.board[X + i][Y + j] == 3:
					return 0 
		return 1


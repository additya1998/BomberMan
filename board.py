from random import randint
from config import *
from os import system
from time import sleep

class Board:

	def __init__(self, BOARD_HEIGHT, BOARD_WIDTH):
		self.board = [[' ' for j in range(BOARD_WIDTH)] for i in range(BOARD_HEIGHT)]
		self.__BOARD_HEIGHT = BOARD_HEIGHT
		self.__BOARD_WIDTH = BOARD_WIDTH

	# Check whether a particular set of co-ordinates belong the the BOARD or not
	def isValid(self, X, Y):
		if X < 0 or Y < 0:
			return 0
		if X + OBJECT_HEIGHT >= self.__BOARD_HEIGHT or Y + OBJECT_WIDTH >= self.__BOARD_WIDTH:
			return 0
		return 1

	# Reset the board to take into consideration any changes
	def reset(self, bomber, enemies, bricks, bomb, powerUps):
		self.board = [[' ' for j in range(BOARD_WIDTH)] for i in range(BOARD_HEIGHT)]
		self.__setWalls()

		# Update position of the bomb
		if bomb:
			if bomb.isActive() and bomb.getShowBlast() == 0:
				for i in range(OBJECT_HEIGHT):
					for j in range(OBJECT_WIDTH):
						self.board[bomb.getX() + i][bomb.getY() + j] = bomb.getTimeLeft()

		# Update the enemies
		for enemy in enemies:
			for i in range(OBJECT_HEIGHT):
				for j in range(OBJECT_WIDTH):
					(health, X, Y) = (enemy.getHealth(), enemy.getX(), enemy.getY())
					if health == 1:
						self.board[X + i][Y + j] = SINGLE_HEALTH_ENEMY_SYMBOL
					elif health == 2:
						self.board[X + i][Y + j] = DOUBLE_HEALTH_ENEMY_SYMBOL

		# Update the bricks
		for brick in bricks:
			if brick.checkDestroyed() == 0:
				for i in range(OBJECT_HEIGHT):
					for j in range(OBJECT_WIDTH):
						self.board[brick.getX() + i][brick.getY() + j] = BRICK_SYMBOL
			else:
				if brick.checkExit():
					for i in range(OBJECT_HEIGHT):
						for j in range(OBJECT_WIDTH):
							self.board[brick.getX() + i][brick.getY() + j] = DOOR_SYMBOL

		# Update the bomber man
		(X, Y) = (bomber.getX(), bomber.getY())
		for i in range(OBJECT_HEIGHT):
			for j in range(OBJECT_WIDTH):
				self.board[bomber.getX() + i][bomber.getY() + j] = BOMBER_MAN_SYMBOL

		# Update the powerups
		for powerUp in powerUps:
			for i in range(OBJECT_HEIGHT):
				for j in range(OBJECT_WIDTH):
					if powerUp.isActive():
						self.board[powerUp.getX() + i][powerUp.getY() + j] = POWER_UP_SYMBOL

		# Update the bomb for an explosion 
		if bomb:
			if bomb.getShowBlast() == 1:

				# Horizontal
				left = bomb.getLength()
				right = bomb.getLength()


				for i in range(bomb.getLength() + 1):
					if self.isValid(bomb.getX(), bomb.getY() - OBJECT_WIDTH * i) == 0:
						left = i - 1
						break
					else:	
						if self.board[bomb.getX()][bomb.getY() - OBJECT_WIDTH * i] == WALL_SYMBOL:
							left = i - 1
							break
						elif self.board[bomb.getX()][bomb.getY() - OBJECT_WIDTH * i] == BRICK_SYMBOL:
							left = i
							break 
					
				for i in range(bomb.getLength() + 1):
					if self.isValid(bomb.getX(), bomb.getY() + OBJECT_WIDTH * i) == 0:
						right = i - 1
						break
					else:	
						if self.board[bomb.getX()][bomb.getY() + OBJECT_WIDTH * i] == WALL_SYMBOL:
							right = i - 1
							break
						elif self.board[bomb.getX()][bomb.getY() + OBJECT_WIDTH * i] == BRICK_SYMBOL:
							right = i
							break

				# Vertical
				up = bomb.getLength()
				down = bomb.getLength()
				for i in range(bomb.getLength() + 1):
					if self.isValid(bomb.getX() - OBJECT_HEIGHT * i, bomb.getY()) == 0:
						up = i - 1
						break
					else:	
						if self.board[bomb.getX() - OBJECT_HEIGHT * i][bomb.getY()] == WALL_SYMBOL:
							up = i - 1
							break
						elif self.board[bomb.getX() - OBJECT_HEIGHT * i][bomb.getY()] == BRICK_SYMBOL:
							up = i
							break
					
				for i in range(bomb.getLength() + 1):
					if self.isValid(bomb.getX() + OBJECT_HEIGHT * i, bomb.getY()) == 0:
						down = i - 1
						break
					else:	
						if self.board[bomb.getX() + OBJECT_HEIGHT * i][bomb.getY()] == WALL_SYMBOL:
							down = i - 1
							break
						elif self.board[bomb.getX() + OBJECT_HEIGHT * i][bomb.getY()] == BRICK_SYMBOL:
							down = i
							break

				# Horizontal
				for i in range(bomb.getY() - OBJECT_WIDTH * left, bomb.getY() + OBJECT_WIDTH * (right + 1)):
					for j in range(bomb.getX(), bomb.getX() + OBJECT_HEIGHT):
						if self.isValid(j, i) and self.board[j][i] != WALL_SYMBOL:
							self.board[j][i] = EXPLOSION_SYMBOL

				# Vertical
				for i in range(bomb.getX() - OBJECT_HEIGHT * up, bomb.getX() + OBJECT_HEIGHT * (down + 1)):
					for j in range(bomb.getY(), bomb.getY() + OBJECT_WIDTH):
						if self.isValid(i, j) and self.board[i][j] != WALL_SYMBOL:
							self.board[i][j] = EXPLOSION_SYMBOL

	# Returns a random empty cell from the board
	def getRandomEmpty(self):
		arr = []
		for i in range(0, self.__BOARD_HEIGHT, 4):
			for j in range(0, self.__BOARD_WIDTH - 2, 4):
				if self.isEmpty(i, j):
					arr.append((i, j))
		return arr[randint(0, len(arr) - 1)]

	# Sets up walls for the game 
	def __setWalls(self):
		for i in range(0, 2):
			for j in range(0, self.__BOARD_WIDTH):
				self.board[i][j] = WALL_SYMBOL
				self.board[self.__BOARD_HEIGHT - i - 1][j] = WALL_SYMBOL

		for i in range(0, self.__BOARD_HEIGHT, 4):
			for j in range(0, self.__BOARD_WIDTH, 8):
				self.board[i][j] = self.board[i][j + 1] = self.board[i][j + 2] = self.board[i][j + 3] = WALL_SYMBOL
				self.board[i + 1][j] = self.board[i + 1][j + 1] = self.board[i + 1][j + 2] = self.board[i + 1][j + 3] = WALL_SYMBOL

		for i in range(0, self.__BOARD_HEIGHT):
			self.board[i][0] = self.board[i][1] = self.board[i][2] = self.board[i][3] = WALL_SYMBOL
			self.board[i][self.__BOARD_WIDTH - 1] = self.board[i][self.__BOARD_WIDTH - 2] = self.board[i][self.__BOARD_WIDTH - 3] = self.board[i][self.__BOARD_WIDTH - 4] = WALL_SYMBOL

	# Displays the board to the user 
	def show(self, level, lives, timeLeft, score):
		system("clear")
		for i in range(0, self.__BOARD_HEIGHT):
			s = ""
			for j in range(0, self.__BOARD_WIDTH):
				x = str(self.board[i][j])
				
				if x == WALL_SYMBOL:
					s = s + BLUE + BLUE_BACKGROUND + x + END
				elif x == BRICK_SYMBOL:
					s = s + GREEN + x + END
				elif x == BOMBER_MAN_SYMBOL:
					s = s + YELLOW + x + END
				elif x == POWER_UP_SYMBOL:
					s = s + GREEN + GREEN_BACKGROUND + x + END
				elif x == EXPLOSION_SYMBOL:
					s = s + YELLOW + x + END
				elif x == '1' or x == '2' or x == '3':
					s = s + RED + x + END
				elif x == DOOR_SYMBOL:
					s = s + WHITE + TURQUOISE_BACKGROUND + x + END
				elif x == SINGLE_HEALTH_ENEMY_SYMBOL:
					s = s + RED  + x + END
				elif x == DOUBLE_HEALTH_ENEMY_SYMBOL:
					s = s + PINK + x + END
				else:
					s = s + x

		print(s)
		print("\n")
		print("CURRENT LEVEL : " + str(level))
		print("LIVES LEFT : " + str(lives))
		print("TIME LEFT : " + str(timeLeft))
		print("SCORE : " + str(score))

	# Checks whether a cell is empty of not
	def isEmpty(self, X, Y):
		if self.isValid(X, Y) == 0:
			return 0

		for i in range(OBJECT_HEIGHT):
			for j in range(OBJECT_WIDTH):
				if self.board[X + i][Y + j] == WALL_SYMBOL or self.board[X + i][Y + j] == BRICK_SYMBOL:
					return 0
				if self.board[X + i][Y + j] == 1 or self.board[X + i][Y + j] == 2 or self.board[X + i][Y + j] == 3:
					return 0 
		return 1


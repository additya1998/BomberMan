from board import * 
from bomb import * 
from config import *
from bomber import *	
from bomb import *	
from enemy import *
from brick import *
from get_input import * 
from random import randint
import sys
import select
from termios import tcflush, TCIOFLUSH
from time import time, sleep


class Game:
	def __init__(self, level, lives, gameTime):

		levelDetails = LEVELS[level]
		self.level = level
		self.lives = lives
		self.gameTime = gameTime
		self.previousGameTime = time()

		self.board = Board(BOARD_HEIGHT, BOARD_WIDTH)
		
		self.bomber = Bomber(START_X, START_Y) 
		self.board.reset(self.bomber, [], [], '')

		self.bricks = []
		for i in range(COUNT_BRICKS):
			(X, Y) = self.board.getRandomEmpty()
			newBrick = Brick(X, Y)
			self.bricks.append(newBrick)
			self.board.reset(self.bomber, [], self.bricks, '')

		self.bricks[randint(0, COUNT_BRICKS - 1)].isExit = 1

		self.bomb = Bomb(0, 0, 0, 0, 0)

		self.enemies = []


		for i in range(levelDetails[0]):
			(X, Y) = self.board.getRandomEmpty()
			newEnemy = Enemy(X, Y, levelDetails[2], levelDetails[4], time())
			self.enemies.append(newEnemy)
			self.board.reset(self.bomber, self.enemies, self.bricks, '')

		for i in range(levelDetails[1]):
			(X, Y) = self.board.getRandomEmpty()
			newEnemy = Enemy(X, Y, levelDetails[3], levelDetails[5], time())
			self.enemies.append(newEnemy)
			self.board.reset(self.bomber, self.enemies, self.bricks, '')

		# exit(0)
		self.board.show(self.level, self.lives, self.gameTime)
		# print(levelDetails[0], levelDetails[1], len(self.enemies))

	def updateTime(self):
		current_time = time()
		if current_time - self.previousGameTime > 1:
			self.gameTime = self.gameTime - 1
			self.previousGameTime = current_time

	def moveEnemies(self):
		current_time = time()
		for enemy in self.enemies:
			if current_time - enemy.prevTime > enemy.speed: 
				enemy.move(self.board)
				enemy.prevTime = current_time
				self.board.reset(self.bomber, self.enemies, self.bricks, self.bomb)
			
		self.board.show(self.level, self.lives, self.gameTime)

	def moveBomber(self, direction):
		self.bomber.moveBomber(direction, self.board)
		self.board.reset(self.bomber, self.enemies, self.bricks, self.bomb)

	def checkSameCell(self):
		for enemy in self.enemies:
			if enemy.X == self.bomber.X and enemy.Y == self.bomber.Y and enemy.health:
				self.bomber.health = self.bomber.health - 1

	def plantBomb(self):
		self.bomb.plantBomb(self.bomber.X, self.bomber.Y)
		self.board.reset(self.bomber, self.enemies, self.bricks, self.bomb)

	def checkBlast(self):
		self.bomb.checkBlast()
		if self.bomb.showBlast and self.bomb.active:
			self.bomb.updateBomb(self.bomber, self.board, self.bricks, self.enemies)
			self.bomb.active = 0
		self.board.reset(self.bomber, self.enemies, self.bricks, self.bomb)
		# self.board.show(self.level, self.lives, self.gameTime)
		# exit(0)

	def checkEnd(self):
		# 0 -> going on
		# 1 -> loose
		# 2 -> win
		if self.gameTime == 0:
			return 1
		if self.bomber.health == 0:
			return 1
		for enemy in self.enemies:
			if enemy.health:
				return 0
		for brick in self.bricks:
			if (brick.X, brick.Y) == (self.bomber.X, self.bomber.Y) and brick.isDestroyed and brick.isExit:
				return 2
		return 0

	
# x = Game(4)
# exit(0)

def startNewGame(currentLevel, gamesLeft):
	game = Game(currentLevel, gamesLeft, GAME_LENGTH)

	previous_bomber = time()
	previous_enemy = time()

	INPUT = Input()

	while True:
		
		sleep(0.09)

		current_time = time()
		seconds = current_time - previous_bomber

		if INPUT.kbhit():
			if seconds > BOMBER_TIME:
				x = INPUT.getch()
				if x == 'w'or x == 'a' or x == 's' or x == 'd':
					game.moveBomber(x)
				elif x == 'b':
					game.plantBomb()
				elif x == 'n':
					# print(currentLevel)
					currentLevel = currentLevel + 1
					# print(currentLevel)
					# exit(0)
					break
			INPUT.flush()
			previous_bomber = current_time

		game.moveEnemies()
		game.checkSameCell()
		game.checkBlast()
		game.updateTime()

		game.board.show(game.level, game.lives, game.gameTime)

		gameStatus = game.checkEnd()
		
		if gameStatus == 0:
			pass

		elif gameStatus == 1:
			gamesLeft = gamesLeft - 1
			return (0, -1)
		
		else:
			currentLevel = currentLevel + 1
			return (1, 1)


(gamesLeft, currentLevel) = (3, 0)
while True:
	if currentLevel > 5:
		print("YOU WIN!")
		break

	elif gamesLeft == 0:
		print("YOU LOOSE!")
		break

	else:
		(X, Y) = startNewGame(currentLevel, gamesLeft)
		currentLevel = currentLevel + X
		gamesLeft = gamesLeft + Y

								
# game = Game(0)

# previous_bomber = time()
# previous_enemy = time()

# INPUT = Input()

# while True:
	
# 	sleep(0.09)

# 	current_time = time()
# 	seconds = current_time - previous_bomber

# 	if INPUT.kbhit():
# 		if seconds > BOMBER_TIME:
# 			x = INPUT.getch()
# 			if x == 'w'or x == 'a' or x == 's' or x == 'd':
# 				game.moveBomber(x)
# 			elif x == 'b':
# 				game.plantBomb()
# 			elif x == 'n':
# 				# print(currentLevel)
# 				currentLevel = currentLevel + 1
# 				# print(currentLevel)
# 				# exit(0)
# 				break
# 		INPUT.flush()
# 		previous_bomber = current_time

# 	game.moveEnemies()
# 	game.checkSameCell()
# 	game.checkBlast()
	
# 	game.board.show(game.level, game.lives, game.gameTime)
# 	# game.board.reset(game.bomber, game.enemies, game.bricks, game.bomb)

# 	gameStatus = game.checkEnd()
	
# 	if gameStatus == 0:
# 		pass

# 	elif gameStatus == 1:
# 		gamesLeft = gamesLeft - 1
# 		break
	
# 	else:
# 		currentLevel = currentLevel + 1
# 		break

						

from board import * 
from bomb import * 
from config import *
from bomber import *	
from bomb import *	
from enemy import *
from brick import *
from get_input import * 
from random import randint
from powerup import *
import sys
import select
from termios import tcflush, TCIOFLUSH
from time import time, sleep


class Game:
	def __init__(self, level, lives, gameTime, previousScore):

		levelDetails = LEVELS[level]
		self.score = previousScore
		self.level = level
		self.lives = lives
		self.gameTime = gameTime
		self.previousGameTime = time()
		self.powerUps = []

		self.board = Board(BOARD_HEIGHT, BOARD_WIDTH)
		
		self.bomber = Bomber(START_X, START_Y) 
		self.board.reset(self.bomber, [], [], '', [])

		self.bricks = []
		for i in range(COUNT_BRICKS):
			(X, Y) = self.board.getRandomEmpty()
			newBrick = Brick(X, Y)
			self.bricks.append(newBrick)
			self.board.reset(self.bomber, [], self.bricks, '', [])

		self.bricks[randint(0, COUNT_BRICKS - 1)].isExit = 1

		self.bomb = Bomb(0, 0, 0, 0, 0)

		self.enemies = []


		for i in range(levelDetails[0]):
			(X, Y) = self.board.getRandomEmpty()
			newEnemy = Enemy(X, Y, levelDetails[2], levelDetails[4], time())
			self.enemies.append(newEnemy)
			self.board.reset(self.bomber, self.enemies, self.bricks, '', [])

		for i in range(levelDetails[1]):
			(X, Y) = self.board.getRandomEmpty()
			newEnemy = Enemy(X, Y, levelDetails[3], levelDetails[5], time())
			self.enemies.append(newEnemy)
			self.board.reset(self.bomber, self.enemies, self.bricks, '', [])

		self.board.show(self.level, self.lives, self.gameTime, self.score)

	def addLife(self):
		(X, Y) = self.board.getRandomEmpty()
		self.powerUps.append(PowerUp(X, Y, time()))

	def updatePowerUp(self):
		for powerUp in self.powerUps:
			powerUp.update()

	def updateTime(self):
		current_time = time()
		if current_time - self.previousGameTime > 1:
			self.gameTime = self.gameTime - 1
			self.previousGameTime = current_time

	def moveEnemies(self):
		current_time = time()
		for enemy in self.enemies:
			if current_time - enemy.prevTime > enemy.speed and enemy.health: 
				enemy.move(self.board)
				enemy.prevTime = current_time
				self.board.reset(self.bomber, self.enemies, self.bricks, self.bomb, self.powerUps)
			
		self.board.show(self.level, self.lives, self.gameTime, self.score)

	def moveBomber(self, direction):
		self.bomber.moveBomber(direction, self.board)
		self.board.reset(self.bomber, self.enemies, self.bricks, self.bomb, self.powerUps)

	def checkSameCell(self):

		for powerUp in self.powerUps:
			if powerUp.isActive:
				if (self.bomber.getX(), self.bomber.getY()) == (powerUp.X, powerUp.Y):
					powerUp.isActive = 0
					self.lives = self.lives + 1
		self.board.reset(self.bomber, self.enemies, self.bricks, self.bomb, self.powerUps)
		# self.board.show(self.level, self.lives, self.gameTime, self.score)
					

		for enemy in self.enemies:
			if enemy.getX() == self.bomber.getX() and enemy.getY() == self.bomber.getY() and enemy.getHealth():
				health = self.bomber.getHealth()
				self.bomber.setHealth(health - 1)

	def plantBomb(self):
		self.bomb.plantBomb(self.bomber.getX(), self.bomber.getY())
		self.board.reset(self.bomber, self.enemies, self.bricks, self.bomb, self.powerUps)

	def checkBlast(self):
		self.bomb.checkBlast()
		if self.bomb.showBlast and self.bomb.active:
			self.score = self.bomb.updateBomb(self.bomber, self.board, self.bricks, self.enemies, self.score)
			self.bomb.active = 0
		self.board.reset(self.bomber, self.enemies, self.bricks, self.bomb, self.powerUps)

	def checkEnd(self):
		# 0 -> going on
		# 1 -> loose
		# 2 -> win
		if self.gameTime == 0:
			return 1
		if self.bomber.getHealth() == 0:
			return 1
		for enemy in self.enemies:
			if enemy.getHealth():
				return 0
		for brick in self.bricks:
			if (brick.X, brick.Y) == (self.bomber.X, self.bomber.Y) and brick.isDestroyed and brick.isExit:
				return 2
		return 0


def startNewGame(currentLevel, gamesLeft, previousScore):
	game = Game(currentLevel, gamesLeft, GAME_LENGTH, previousScore)

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
				elif x == 'q':
					exit(0)
				elif x == 'p':
					game.addLife()
			INPUT.flush()
			previous_bomber = current_time

		game.moveEnemies()
		game.checkSameCell()
		game.checkBlast()
		game.updateTime()
		game.updatePowerUp()

		game.board.show(game.level, game.lives, game.gameTime, game.score)

		gameStatus = game.checkEnd()
		
		if gameStatus == 0:
			pass

		elif gameStatus == 1:
			gamesLeft = gamesLeft - 1
			return (0, -1, game.score)
		
		else:
			currentLevel = currentLevel + 1
			return (1, 1, game.score + game.gameTime)


(gamesLeft, currentLevel, initialScore) = (3, 0, 0)
while True:
	if currentLevel > 5:
		print("YOU WIN!")
		break

	elif gamesLeft == 0:
		print("YOU LOOSE!")
		break

	else:
		(X, Y, SCORE) = startNewGame(currentLevel, gamesLeft, initialScore)
		currentLevel = currentLevel + X
		gamesLeft = gamesLeft + Y
		initialScore = SCORE

								

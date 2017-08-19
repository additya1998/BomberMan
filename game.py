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
	def __init__(self, level):
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
		for i in range(COUNT_ENEMEIES):
			(X, Y) = self.board.getRandomEmpty()
			if level == 1:
				newEnemy = Enemy(X, Y, 1, 1)
			else:
				newEnemy = Enemy(X, Y, randint(1, 2), 1)
			self.enemies.append(newEnemy)
			self.board.reset(self.bomber, self.enemies, self.bricks, '')

		self.board.show()

	def moveEnemies(self):
		for i in range(len(self.enemies)):
			self.enemies[i].move(self.board)
			self.board.reset(self.bomber, self.enemies, self.bricks, self.bomb)
			
		self.board.show()

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
		if self.bomb.showBlast == 1:
			self.updateBomb()

	def updateBomb(self):
		# print("LOL")
		# exit(0)
		# UP
		f = 1
		for i in range(0, self.bomb.length):
			(X, Y) = (self.bomb.X - i * OBJECT_HEIGHT, self.bomb.Y)
			if self.board.isValid(X, Y):
				if self.board.board[X][Y] == 'X':
					f = 0
					break
				for brick in self.bricks:
					if (brick.X, brick.Y) == (X, Y) and brick.isDestroyed == 0:
						brick.isDestroyed = 1
						# print(brick.X, brick.Y)
						f = 0
						break
				if f == 0:
					break
				for enemy in self.enemies:
					if (enemy.X, enemy.Y) == (X, Y) and enemy.health > 0:
						enemy.health = enemy.health - 1
						
				if (X, Y) == (self.bomber.X, self.bomber.Y):
					self.bomber.health = self.bomber.health - 1		

		# DOWN
		f = 1
		for i in range(0, self.bomb.length):
			(X, Y) = (self.bomb.X + i * OBJECT_HEIGHT, self.bomb.Y)
			if self.board.isValid(X, Y):
				if self.board.board[X][Y] == 'X':
					f = 0
					break
				for brick in self.bricks:
					if (brick.X, brick.Y) == (X, Y) and brick.isDestroyed == 0:
						brick.isDestroyed = 1
						# print(brick.X, brick.Y)
						f = 0
						break
				if f == 0:
					break
				for enemy in self.enemies:
					if (enemy.X, enemy.Y) == (X, Y) and enemy.health > 0:
						enemy.health = enemy.health - 1
						
				if (X, Y) == (self.bomber.X, self.bomber.Y) and self.bomber.health > 0:
					self.bomber.health = self.bomber.health - 1		

		# LEFT
		f = 1
		for i in range(0, self.bomb.length):
			(X, Y) = (self.bomb.X, self.bomb.Y - i * OBJECT_WIDTH)
			if self.board.isValid(X, Y):
				if self.board.board[X][Y] == 'X':
					f = 0
					break
				for brick in self.bricks:
					if (brick.X, brick.Y) == (X, Y) and brick.isDestroyed == 0:
						brick.isDestroyed = 1
						# print(brick.X, brick.Y)
						f = 0
						break
				if f == 0:
					break
				for enemy in self.enemies:
					if (enemy.X, enemy.Y) == (X, Y) and enemy.health > 0:
						enemy.health = enemy.health - 1
						
				if (X, Y) == (self.bomber.X, self.bomber.Y) and self.bomber.health > 0:
					self.bomber.health = self.bomber.health - 1		

		# RIGHT
		f = 1
		for i in range(0, self.bomb.length):
			(X, Y) = (self.bomb.X, self.bomb.Y + i * OBJECT_WIDTH)
			if self.board.isValid(X, Y):
				if self.board.board[X][Y] == 'X':
					f = 0
					break
				for brick in self.bricks:
					if (brick.X, brick.Y) == (X, Y) and brick.isDestroyed == 0:
						brick.isDestroyed = 1
						# print(brick.X, brick.Y)
						f = 0
						break
				if f == 0:
					break
				for enemy in self.enemies:
					if (enemy.X, enemy.Y) == (X, Y) and enemy.health > 0:
						enemy.health = enemy.health - 1
						
				if (X, Y) == (self.bomber.X, self.bomber.Y) and self.bomber.health > 0:
					self.bomber.health = self.bomber.health - 1		
		# print("EXIT")
		# exit(0)
		self.board.reset(self.bomber, self.enemies, self.bricks, self.bomb)

	def checkHealth(self):
		return self.bomber.health

	def checkEnd(self):
		for enemy in self.enemies:
			if enemy.health:
				return 0
		for brick in self.bricks:
			if (brick.X, brick.Y) == (self.bomber.X, self.bomber.Y) and brick.isDestroyed and brick.isExit:
				return 1
		return 0

def endGame():
	game.board.reset(game.bomber, game.enemies, game.bricks, game.bomb)
	game.board.show
	# system("tput reset")
	print("Game Over")
	


game = Game(1)

previous_bomber = time()
previous_enemy = time()

INPUT = Input()
yes = 0

while True:
	
	sleep(0.05)

	current_time = time()
	seconds = current_time - previous_bomber

	if INPUT.kbhit():
		if seconds > BOMBER_TIME:
			x = INPUT.getch()
			if x == 'w'or x == 'a' or x == 's' or x == 'd':
				game.moveBomber(x)
			elif x == 'b':
				yes = 1
				game.plantBomb()
		INPUT.flush()
		previous_bomber = current_time

	seconds = current_time - previous_enemy
	

	if seconds > ENEMY_TIME:
		game.moveEnemies()
		previous_enemy = current_time

	game.checkSameCell()
	game.checkBlast()
	
	if game.checkHealth() == 0:
		endGame()
		break

	if game.checkEnd():
		endGame()
		break



	




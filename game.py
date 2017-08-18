from board import * 
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
from time import time


class Game:
	def __init__(self, level):
		self.board = Board(BOARD_HEIGHT, BOARD_WIDTH)
		
		self.bomber = Bomber(START_X, START_Y) 
		self.board.reset(self.bomber)

		self.bricks = []
		for i in range(COUNT_BRICKS):
			(X, Y) = self.board.getRandomEmpty()
			newBrick = Brick(X, Y)
			self.bricks.append(newBrick)
			self.board.reset(self.bomber, [], self.bricks)

		self.bricks[randint(0, COUNT_BRICKS - 1)].isExit = 1

		self.bomb = Bomb(0, 0, 0, 0)

		self.enemies = []
		for i in range(COUNT_ENEMEIES):
			(X, Y) = self.board.getRandomEmpty()
			if level == 1:
				newEnemy = Enemy(X, Y, 0, 1)
			else:
				newEnemy = Enemy(X, Y, randint(0, 1), 1)
			self.enemies.append(newEnemy)
			self.board.reset(self.bomber, self.enemies, self.bricks)

		self.board.show()

	def moveEnemies(self):
		for i in range(len(self.enemies)):
			self.enemies[i].move(self.board)
			self.board.reset(self.bomber, self.enemies, self.bricks)
			
		self.board.show()

	def moveBomber(self, direction):
		self.bomber.moveBomber(direction, self.board)
		self.board.reset(self.bomber, self.enemies, self.bricks)

	def checkSameCell(self):
		for enemy in self.enemies:
			if enemy.X == self.bomber.X and enemy.Y == self.bomber.Y:
				return 1
		return 0


game = Game(2)

previous_bomber = time()
previous_enemy = time()

INPUT = Input()

while True:
	
	current_time = time()
	seconds = current_time - previous_bomber

	if seconds > BOMBER_TIME:
		if INPUT.kbhit() :
			x = INPUT.getch()
			INPUT.flush()
			if x == 'w'or x == 'a' or x == 's' or x == 'd':
				game.moveBomber(x)
		previous_bomber = current_time

	seconds = current_time - previous_enemy
	if seconds > ENEMY_TIME:
		game.moveEnemies()
		previous_enemy = current_time

	if game.checkSameCell():
		system("tput reset")
		print("Game Over")
		break

	




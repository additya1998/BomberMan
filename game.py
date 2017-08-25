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
        self.__score = previousScore
        self.__level = level
        self.__lives = lives
        self.__gameTime = gameTime
        self.__previousGameTime = time()
        self.__powerUps = []

        # Object of the board class that contains the board details for the
        # current game
        self.__board = Board(BOARD_HEIGHT, BOARD_WIDTH)

        # Object of the bomber class that contains the details for the
        # bomberman for the current game
        self.__bomber = Bomber(START_X, START_Y)
        self.__board.reset(self.__bomber, [], [], '', [])

        # Adding bricks to the game
        self.__bricks = []
        for i in range(COUNT_BRICKS):
            (X, Y) = self.__board.getRandomEmpty()
            newBrick = Brick(X, Y)
            self.__bricks.append(newBrick)
            self.__board.reset(self.__bomber, [], self.__bricks, '', [])

        # Setting a brick as the Door to the next level for the current game
        self.__bricks[randint(0, COUNT_BRICKS - 1)].setExit()

        # Initialising a bomb for the game, which is initially inactive
        self.__bomb = Bomb(0, 0, 0, 0, 0)

        self.__enemies = []

        # Add enemies with single health
        for i in range(levelDetails[0]):
            (X, Y) = self.__board.getRandomEmpty()
            newEnemy = Enemy(X, Y, levelDetails[2], levelDetails[4], time())
            self.__enemies.append(newEnemy)
            self.__board.reset(self.__bomber, self.__enemies, self.__bricks,
                               '', [])

        # Add enemies with double health
        for i in range(levelDetails[1]):
            (X, Y) = self.__board.getRandomEmpty()
            newEnemy = Enemy(X, Y, levelDetails[3], levelDetails[5], time())
            self.__enemies.append(newEnemy)
            self.__board.reset(self.__bomber, self.__enemies, self.__bricks,
                               '', [])

    # Getter functions

    def getLevel(self):
        return self.__level

    def getScore(self):
        return self.__score

    def getLives(self):
        return self.__lives

    def getGameTime(self):
        return self.__gameTime

    def show(self):
        self.__board.show(self.__level, self.__lives, self.__gameTime,
                          self.__score)

    # To increment available lives for the player
    def addLife(self):
        (X, Y) = self.__board.getRandomEmpty()
        self.__powerUps.append(PowerUp(X, Y, time()))

    # Update all the powerups
    def updatePowerUp(self):
        for powerUp in self.__powerUps:
            powerUp.update()

    def updateTime(self):
        current_time = time()
        if current_time - self.__previousGameTime > 1:
            self.__gameTime = self.__gameTime - 1
            self.__previousGameTime = current_time

    # Chooses a random empty adjacent block and moves an enemy to it
    def moveEnemies(self):
        current_time = time()
        for enemy in self.__enemies:
            if current_time - enemy.getPrevTime() > enemy.getSpeed():
                if enemy.getHealth():

                    (X, Y) = (enemy.getX(), enemy.getY())
                    arr = []

                    if self.__board.isEmpty(X - OBJECT_HEIGHT, Y):
                        arr.append((-OBJECT_HEIGHT, 0))

                    if self.__board.isEmpty(X + OBJECT_HEIGHT, Y):
                        arr.append((OBJECT_HEIGHT, 0))

                    if self.__board.isEmpty(X, Y - OBJECT_WIDTH):
                        arr.append((0, -OBJECT_WIDTH))

                    if self.__board.isEmpty(X, Y + OBJECT_WIDTH):
                        arr.append((0, OBJECT_WIDTH))

                    if len(arr) == 0:
                        pass
                    else:
                        idx = arr[randint(0, len(arr) - 1)]
                        (x, y) = idx
                        enemy.move(X + x, Y + y)

                    enemy.setPrevTime(current_time)
                    self.__board.reset(self.__bomber, self.__enemies,
                                       self.__bricks, self.__bomb,
                                       self.__powerUps)

    # Move the bomber in the specified direction if possible
    def moveBomber(self, direction):

        (X, Y) = (self.__bomber.getX(), self.__bomber.getY())
        if direction == 'w' or direction == 'W':
            if self.__board.isEmpty(X - OBJECT_HEIGHT, Y):
                self.__bomber.move(X - OBJECT_HEIGHT, Y)

        elif direction == 'a' or direction == 'A':
            if self.__board.isEmpty(X, Y - OBJECT_WIDTH):
                self.__bomber.move(X, Y - OBJECT_WIDTH)

        elif direction == 's' or direction == 'S':
            if self.__board.isEmpty(X + OBJECT_HEIGHT, Y):
                self.__bomber.move(X + OBJECT_HEIGHT, Y)

        elif direction == 'd' or direction == 'D':
            if self.__board.isEmpty(X, Y + OBJECT_WIDTH):
                self.__bomber.move(X, Y + OBJECT_WIDTH)

        self.__board.reset(self.__bomber, self.__enemies, self.__bricks,
                           self.__bomb, self.__powerUps)

    # Check whether the BomberMan is in the same cell with an enemy, powerup,
    # or explosion
    def checkSameCell(self):

        for powerUp in self.__powerUps:
            if powerUp.isActive():
                (X, Y) = (self.__bomber.getX(), self.__bomber.getY())
                (x, y) = (powerUp.getX(), powerUp.getY())
                if (X, Y) == (x, y):
                    powerUp.setInActive()
                    self.__lives = self.__lives + 1
        self.__board.reset(self.__bomber, self.__enemies, self.__bricks,
                           self.__bomb, self.__powerUps)

        for enemy in self.__enemies:
            (X, Y) = (enemy.getX(), enemy.getY())
            (x, y) = (self.__bomber.getX(), self.__bomber.getY())
            if (X, Y) == (x, y) and enemy.getHealth():
                health = self.__bomber.getHealth()
                self.__bomber.setHealth(health - 1)

    def plantBomb(self):
        self.__bomb.plantBomb(self.__bomber.getX(), self.__bomber.getY())
        self.__board.reset(self.__bomber, self.__enemies, self.__bricks,
                           self.__bomb, self.__powerUps)

    def checkBlast(self):
        self.__bomb.checkBlast()
        if self.__bomb.getShowBlast() and self.__bomb.isActive():
            self.__score = self.__bomb.update(self.__bomber, self.__board,
                                              self.__bricks, self.__enemies,
                                              self.__score)
            self.__bomb.makeInactive()
        self.__board.reset(self.__bomber, self.__enemies, self.__bricks,
                           self.__bomb, self.__powerUps)

    # Check whether the game should end now
    # 0 -> going on
    # 1 -> loose
    # 2 -> win
    def checkEnd(self):
        if self.__gameTime == 0:
            return 1
        if self.__bomber.getHealth() == 0:
            return 1
        for enemy in self.__enemies:
            if enemy.getHealth():
                return 0
        for brick in self.__bricks:
            (X, Y) = (brick.getX(), brick.getY())
            (x, y) = (self.__bomber.getX(), self.__bomber.getY())

            if (X, Y) == (x, y) and brick.checkDestroyed():
                if brick.checkExit():
                    return 2
        return 0


def startNewGame(currentLevel, gamesLeft, previousScore):
    game = Game(currentLevel, gamesLeft, GAME_LENGTH, previousScore)

    previous_bomber = time()
    previous_enemy = time()

    INPUT = Input()

    while True:

        sleep(0.1)

        current_time = time()
        seconds = current_time - previous_bomber

        if INPUT.checkStream():
            if seconds > BOMBER_TIME:
                x = INPUT.getFromStream()
                if x == 'w'or x == 'a' or x == 's' or x == 'd':
                    game.moveBomber(x)
                elif x == 'b':
                    game.plantBomb()
                elif x == 'q':
                    
                    exit(0)
                elif x == 'p':
                    game.addLife()
            INPUT.clearStream()
            previous_bomber = current_time

        game.moveEnemies()
        game.checkSameCell()
        game.checkBlast()
        game.updateTime()
        game.updatePowerUp()

        game.show()

        gameStatus = game.checkEnd()

        if gameStatus == 0:
            pass

        elif gameStatus == 1:
            gamesLeft = gamesLeft - 1
            return (0, -1, game.getScore())

        else:
            currentLevel = currentLevel + 1
            return (1, 1, game.getScore() + game.getGameTime())


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

from position import *
from time import time
from config import *


# A class that contains the details about the bomb.
class Bomb(Position):
    def __init__(self, X, Y, timeLeft, active, previousTime, length=EXPLOSION_LENGTH):
        Position.__init__(self, X, Y)
        # Time left before explosion
        self.__timeLeft = timeLeft

        # Whether bomb is active or not
        self.__active = active

        # Time when it was previously updated
        self.__previousTime = previousTime

        # Length of the explosion
        self.__length = length

        # Whether the explosion has to be displayed or not
        self.__showBlast = 0

        # Time when explosion took place
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
        # To update time before explosion
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

        # To check for how long the blast has been displayed
        if self.__showBlast:
            current_time = time()
            if current_time - self.__blastTime > BOMB_TIME_LENGTH:
                self.__timeLeft = 0
                self.__active = 0
                self.__previousTime = 0
                self.__showBlast = 0
                self.__blastTime = 0

    def update(self, bomber, board, bricks, enemies, score):

        # Checkig in the upwards direction for the effect of the BOMB
        f = 1
        for i in range(self.__length + 1):
            (X, Y) = (self.getX() - i * OBJECT_HEIGHT, self.getY())
            if board.isValid(X, Y):
                # Stop if it is a wall, since explosions cannot pass throught walls
                if board.board[X][Y] == WALL_SYMBOL:
                    f = 0
                    break

                # Check if a brick is affected or not, and if yes, add it to the score and stop since
                # effect of explosion won't pass through a brick
                for brick in bricks:
                    if (brick.getX(), brick.getY()) == (X, Y) and brick.checkDestroyed() == 0:
                        brick.setDestroyed()
                        score = score + BRICK_SCORE
                        f = 0
                        break
                if f == 0:
                    break

                # Kill enemies which are within the range of the explosion
                for enemy in enemies:
                    if (enemy.getX(), enemy.getY()) == (X, Y) and enemy.getHealth() > 0:
                        enemy.setHealth(enemy.getHealth() - 1)
                        if enemy.getHealth() == 0:
                            score = score + ENEMY_SCORE

                # Decrement the health of the BomberMan if he is in range of the explosion
                if (X, Y) == (bomber.getX(), bomber.getY()):
                    bomber.setHealth(bomber.getHealth() - 1)

        # Checkig in the downwards direction for the effect of the BOMB
        f = 1
        for i in range(self.__length + 1):
            (X, Y) = (self.getX() + i * OBJECT_HEIGHT, self.getY())
            if board.isValid(X, Y):
                # Stop if it is a wall, since explosions cannot pass throught walls
                if board.board[X][Y] == WALL_SYMBOL:
                    f = 0
                    break

                # Check if a brick is affected or not, and if yes, add it to the score and stop since
                # effect of explosion won't pass through a brick
                for brick in bricks:
                    if (brick.getX(), brick.getY()) == (X, Y) and brick.checkDestroyed() == 0:
                        brick.setDestroyed()
                        score = score + BRICK_SCORE
                        f = 0
                        break
                if f == 0:
                    break

                # Kill enemies which are within the range of the explosion
                for enemy in enemies:
                    if (enemy.getX(), enemy.getY()) == (X, Y) and enemy.getHealth() > 0:
                        enemy.setHealth(enemy.getHealth() - 1)
                        if enemy.getHealth() == 0:
                            score = score + ENEMY_SCORE

                # Decrement the health of the BomberMan if he is in range of the explosion
                if (X, Y) == (bomber.getX(), bomber.getY()) and bomber.getHealth() > 0:
                    bomber.setHealth(bomber.getHealth() - 1)

        # Checkig in the left direction for the effect of the BOMB
        f = 1
        for i in range(self.__length + 1):
            (X, Y) = (self.getX(), self.getY() - i * OBJECT_WIDTH)
            if board.isValid(X, Y):
                # Stop if it is a wall, since explosions cannot pass throught walls
                if board.board[X][Y] == WALL_SYMBOL:
                    f = 0
                    break

                # Check if a brick is affected or not, and if yes, add it to the score and stop since
                # effect of explosion won't pass through a brick
                for brick in bricks:
                    if (brick.getX(), brick.getY()) == (X, Y) and brick.checkDestroyed() == 0:
                        brick.setDestroyed()
                        score = score + BRICK_SCORE
                        f = 0
                        break
                if f == 0:
                    break

                # Kill enemies which are within the range of the explosion
                for enemy in enemies:
                    if (enemy.getX(), enemy.getY()) == (X, Y) and enemy.getHealth() > 0:
                        enemy.setHealth(enemy.getHealth() - 1)
                        if enemy.getHealth() == 0:
                            score = score + ENEMY_SCORE

                # Decrement the health of the BomberMan if he is in range of the explosion
                if (X, Y) == (bomber.getX(), bomber.getY()) and bomber.getHealth() > 0:
                    bomber.setHealth(bomber.getHealth() - 1)

        # Checkig in the right direction for the effect of the BOMB
        f = 1
        for i in range(self.__length + 1):
            (X, Y) = (self.getX(), self.getY() + i * OBJECT_WIDTH)
            if board.isValid(X, Y):
                # Stop if it is a wall, since explosions cannot pass throught walls
                if board.board[X][Y] == WALL_SYMBOL:
                    f = 0
                    break

                # Check if a brick is affected or not, and if yes, add it to the score and stop since
                # effect of explosion won't pass through a brick
                for brick in bricks:
                    if (brick.getX(), brick.getY()) == (X, Y) and brick.checkDestroyed() == 0:
                        brick.setDestroyed()
                        score = score + BRICK_SCORE
                        f = 0
                        break
                if f == 0:
                    break

                # Kill enemies which are within the range of the explosion
                for enemy in enemies:
                    if (enemy.getX(), enemy.getY()) == (X, Y) and enemy.getHealth() > 0:
                        enemy.setHealth(enemy.getHealth() - 1)
                        if enemy.getHealth() == 0:
                            score = score + ENEMY_SCORE

                # Decrement the health of the BomberMan if he is in range of the explosion
                if (X, Y) == (bomber.getX(), bomber.getY()) and bomber.getHealth() > 0:
                    bomber.setHealth(bomber.getHealth() - 1)

        return score

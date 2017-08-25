from random import randint
from config import *
from os import system
from time import sleep


class Board:

    def __init__(self, BOARD_HEIGHT, BOARD_WIDTH):
        self.board = [[' ' for j in range(BOARD_WIDTH)]
                      for i in range(BOARD_HEIGHT)]
        self.__BOARD_HEIGHT = BOARD_HEIGHT
        self.__BOARD_WIDTH = BOARD_WIDTH

    # Check whether a particular set of co-ordinates belong the the BOARD or
    # not
    def isValid(self, X, Y):
        if X < 0 or Y < 0:
            return 0
        if X + OBJECT_HEIGHT >= self.__BOARD_HEIGHT:
            return 0
        if Y + OBJECT_WIDTH >= self.__BOARD_WIDTH:
            return 0
        return 1

    # Reset the board to take into consideration any changes
    def reset(self, bomber, enemies, bricks, bomb, powerUps):
        self.board = [[' ' for j in range(BOARD_WIDTH)]
                      for i in range(BOARD_HEIGHT)]
        self.__setWalls()

        # Update position of the bomb
        if bomb:
            if bomb.isActive() and bomb.getShowBlast() == 0:
                (X, Y) = (bomb.getX(), bomb.getY())
                for i in range(OBJECT_HEIGHT):
                    for j in range(OBJECT_WIDTH):
                        self.board[X + i][Y + j] = bomb.getTimeLeft()

        # Update the enemies
        for enemy in enemies:
            health = enemy.getHealth()
            (X, Y) = (enemy.getX(), enemy.getY())
            for i in range(OBJECT_HEIGHT):
                for j in range(OBJECT_WIDTH):
                    if health == 1:
                        self.board[X + i][Y + j] = SINGLE_HEALTH_ENEMY_SYMBOL
                    elif health == 2:
                        self.board[X + i][Y + j] = DOUBLE_HEALTH_ENEMY_SYMBOL

        # Update the bricks
        for brick in bricks:
            (X, Y) = (brick.getX(), brick.getY())
            if brick.checkDestroyed() == 0:
                for i in range(OBJECT_HEIGHT):
                    for j in range(OBJECT_WIDTH):
                        self.board[X + i][Y + j] = BRICK_SYMBOL
            else:
                if brick.checkExit():
                    for i in range(OBJECT_HEIGHT):
                        for j in range(OBJECT_WIDTH):
                            self.board[X + i][Y + j] = DOOR_SYMBOL

        # Update the bomber man
        (X, Y) = (bomber.getX(), bomber.getY())
        for i in range(OBJECT_HEIGHT):
            for j in range(OBJECT_WIDTH):
                self.board[X + i][Y + j] = BOMBER_MAN_SYMBOL

        # Update the powerups
        for powerUp in powerUps:
            (X, Y) = (powerUp.getX(), powerUp.getY())
            for i in range(OBJECT_HEIGHT):
                for j in range(OBJECT_WIDTH):
                    if powerUp.isActive():
                        self.board[X + i][Y + j] = POWER_UP_SYMBOL

        # Update the bomb for an explosion
        if bomb:

            (X, Y) = (bomb.getX(), bomb.getY())

            if bomb.getShowBlast() == 1:

                # Horizontal
                left = bomb.getLength()
                right = bomb.getLength()

                for i in range(bomb.getLength() + 1):
                    y_c = Y - (OBJECT_WIDTH * i)
                    if self.isValid(X, y_c) == 0:
                        left = i - 1
                        break
                    else:
                        if self.board[X][y_c] == WALL_SYMBOL:
                            left = i - 1
                            break
                        elif self.board[X][y_c] == BRICK_SYMBOL:
                            left = i
                            break

                for i in range(bomb.getLength() + 1):
                    y_c = Y + (OBJECT_WIDTH * i)
                    if self.isValid(X, y_c) == 0:
                        right = i - 1
                        break
                    else:
                        if self.board[X][y_c] == WALL_SYMBOL:
                            right = i - 1
                            break
                        elif self.board[X][y_c] == BRICK_SYMBOL:
                            right = i
                            break

                # Vertical
                up = bomb.getLength()
                down = bomb.getLength()
                for i in range(bomb.getLength() + 1):
                    x_c = X - (OBJECT_HEIGHT * i)
                    if self.isValid(x_c, Y) == 0:
                        up = i - 1
                        break
                    else:
                        if self.board[x_c][Y] == WALL_SYMBOL:
                            up = i - 1
                            break
                        elif self.board[x_c][Y] == BRICK_SYMBOL:
                            up = i
                            break

                for i in range(bomb.getLength() + 1):
                    x_c = X + (OBJECT_HEIGHT * i)
                    if self.isValid(x_c, Y) == 0:
                        down = i - 1
                        break
                    else:
                        if self.board[x_c][Y] == WALL_SYMBOL:
                            down = i - 1
                            break
                        elif self.board[x_c][Y] == BRICK_SYMBOL:
                            down = i
                            break

                # Horizontal
                r_l = Y - OBJECT_WIDTH * left
                r_r = Y + OBJECT_WIDTH * (right + 1)
                for i in range(r_l, r_r):
                    for j in range(X, X + OBJECT_HEIGHT):
                        if self.isValid(j, i):
                            if self.board[j][i] != WALL_SYMBOL:
                                self.board[j][i] = EXPLOSION_SYMBOL

                # Vertical
                r_l = X - OBJECT_HEIGHT * up
                r_r = X + OBJECT_HEIGHT * (down + 1)
                for i in range(r_l, r_r):
                    for j in range(Y, Y + OBJECT_WIDTH):
                        if self.isValid(i, j):
                            if self.board[i][j] != WALL_SYMBOL:
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
                self.board[i][j] = WALL_SYMBOL
                self.board[i][j + 1] = WALL_SYMBOL
                self.board[i][j + 2] = WALL_SYMBOL
                self.board[i][j + 3] = WALL_SYMBOL
                self.board[i + 1][j] = WALL_SYMBOL
                self.board[i + 1][j + 1] = WALL_SYMBOL
                self.board[i + 1][j + 2] = WALL_SYMBOL
                self.board[i + 1][j + 3] = WALL_SYMBOL

        for i in range(0, self.__BOARD_HEIGHT):
            self.board[i][0] = WALL_SYMBOL
            self.board[i][1] = WALL_SYMBOL
            self.board[i][2] = WALL_SYMBOL
            self.board[i][3] = WALL_SYMBOL
            self.board[i][self.__BOARD_WIDTH - 1] = WALL_SYMBOL
            self.board[i][self.__BOARD_WIDTH - 2] = WALL_SYMBOL
            self.board[i][self.__BOARD_WIDTH - 3] = WALL_SYMBOL
            self.board[i][self.__BOARD_WIDTH - 4] = WALL_SYMBOL

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
                    s = s + RED + x + END
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
                if self.board[X + i][Y + j] == WALL_SYMBOL:
                    return 0
                elif self.board[X + i][Y + j] == BRICK_SYMBOL:
                    return 0
                elif self.board[X + i][Y + j] == 1:
                    return 0
                elif self.board[X + i][Y + j] == 2:
                    return 0
                elif self.board[X + i][Y + j] == 3:
                    return 0
        return 1

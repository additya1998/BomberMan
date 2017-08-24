# Class that is inherited by various other classes to manage their positions on the board.


class Position:
    def __init__(self, X, Y):
        self.__X = X
        self.__Y = Y

    def getX(self):
        return self.__X

    def getY(self):
        return self.__Y

    def setX(self, value):
        self.__X = value

    def setY(self, value):
        self.__Y = value

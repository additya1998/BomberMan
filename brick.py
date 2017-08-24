from position import *


# A class for the brick objects
class Brick(Position):
    def __init__(self, X, Y, isExit=0, isDestroyed=0):
        Position.__init__(self, X, Y)
        self.__isExit = isExit
        self.__isDestroyed = isDestroyed

    # Check whether this is brick is the door to the next level
    def checkExit(self):
        return self.__isExit

    # Check whether this brick is destroyed
    def checkDestroyed(self):
        return self.__isDestroyed

    # Destroy brick
    def setDestroyed(self):
        self.__isDestroyed = 1

    # Make the buick the door to the next level
    def setExit(self):
        self.__isExit = 1

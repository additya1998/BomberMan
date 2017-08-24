from time import time
from config import POWER_UP_LENGTH
from position import*


# Class to manage the time of spawned power-ups
class PowerUp(Position):
    def __init__(self, X, Y, previousTime):
        Position.__init__(self, X, Y)
        self.__previousTime = previousTime
        self.__active = 1

    # Check whether the power-up has timed out or not
    def update(self):
        current_time = time()
        if current_time - self.__previousTime > POWER_UP_LENGTH:
            self.__active = 0

    # To check whether the power-up is active or not, and to make it inative after some time.

    def isActive(self):
        return self.__active

    def setInActive(self):
        self.__active = 0

from position import *

# Class that inherits the Position class and also has a data member health
# and function like move that is common to both the BomberMan and the Enemy
# class


class Person(Position):
    def __init__(self, X, Y, health):
        Position.__init__(self, X, Y)
        self.__health = health

    def getHealth(self):
        return self.__health

    def setHealth(self, value):
        self.__health = value

    def move(self, X, Y):
        self.setX(X)
        self.setY(Y)

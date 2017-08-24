from person import *
from config import *


# A class whose instance is the BomberMan
class Bomber(Person):

    def __init__(self, X, Y):
        Person.__init__(self, X, Y, health=1)
        self.speed = 0

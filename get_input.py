import sys
import termios
from select import select


class Input:

    def __init__(self):
        self.__fileDescriptor = sys.stdin.fileno()
        self.__newTerm = termios.tcgetattr(self.__fileDescriptor)
        self.__oldTerm = termios.tcgetattr(self.__fileDescriptor)
        self.__newTerm[3] = (self.__newTerm[3] & ~termios.ICANON & ~termios.ECHO)
        termios.tcsetattr(self.__fileDescriptor, termios.TCSAFLUSH, self.__newTerm)

    def kbhit(self):
        dr, dw, de = select([sys.stdin], [], [], 0)
        return dr != []

    def getch(self):
        return sys.stdin.read(1)

    def flush(self):
        termios.tcflush(self.__fileDescriptor, termios.TCIFLUSH)

    def __del__(self):
        termios.tcsetattr(self.__fileDescriptor, termios.TCSANOW, self.__oldTerm)

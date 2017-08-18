import sys, termios
from select import select

class Input:

	def __init__(self):
		self.fileDescriptor = sys.stdin.fileno()
		self.newTerm = termios.tcgetattr(self.fileDescriptor)
		self.oldTerm = termios.tcgetattr(self.fileDescriptor)

		self.newTerm[3] = (self.newTerm[3] & ~termios.ICANON & ~termios.ECHO)
		termios.tcsetattr(self.fileDescriptor, termios.TCSAFLUSH, self.newTerm)
	def kbhit(self):
		dr, dw, de = select([sys.stdin], [], [], 0)
		return dr != []

	def getch(self):
		return sys.stdin.read(1)

	def flush(self):
		termios.tcflush(self.fileDescriptor, termios.TCIFLUSH)

	def __del__(self):	
		termios.tcsetattr(self.fileDescriptor, termios.TCSANOW, self.oldTerm)

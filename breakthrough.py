import numpy as np
import heapq
import timeit
import sys
import pdb

class Game(object):

	height = 8
	width = 8
	size = 64
	board = []

	def __init__(self):
		setup = []
		for i in range(self.size):
			if i < 16:
				setup.append(Piece("black"))
			elif i >= 16 and i < 48:
				setup.append(Piece(""))
			else:
				setup.append(Piece("white"))
		self.board = np.array(setup).reshape(8,8)


	def printBoard(self):
		for i in range(self.height):
			for j in range(self.width):
				if game.board[i][j].color == "black":
					print 'B',
				elif game.board[i][j].color == "white":
					print 'W',
				else:
					print ' ',
			print ''



class Piece(object):

	color = ""
	

	def __init__(self, color):
		self.color = color



'''Main function routine'''
game = Game()
game.printBoard()
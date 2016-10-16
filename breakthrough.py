import numpy as np
import heapq
import timeit
import sys
import pdb
import copy




class Game(object):

	#some private variables; could add more
	height = 8
	width = 8
	size = 64
	board = []

	def __init__(self):
		setup = []
		#we begin by initialize the start of the board
		for i in range(self.height):
			for j in range(self.width):
				if i < 2:
					setup.append(Piece("black", j, i))
				elif i > 5:
					setup.append(Piece("white", j, i))
				else:
					setup.append(Piece("", j, i))
		#we represent the board as a 2D-array
		self.board = np.array(setup).reshape(8,8)

	def getPiece(self, x, y):
		# (0,0) = piece at top-left corner
		# (0,7) = piece at bottom-left corner
		# (7,0) = piece at top-right corner
		'''I think the placement of the "x" and "y" parameters may make calling cell positions
				a little confusing. Might consider switching these placements to be more consistent
					(i.e. --> getPiece(self, y, x)  OR getPiece(self, col, row)) but idk...'''
		i = y
		j = x
		return self.board[i][j]

	def moveF(self, piece):
		#move a piece forward
		x = piece.xpos
		y = piece.ypos
		if((piece.color == "white") and ((y - 1) >= 0) and (self.getPiece(x, y - 1).color == "")):
			#moving "up" board
			movedPiece = copy.deepcopy(self.getPiece(x, y))
			self.board[y][x] = Piece("", x, y)	#make this moved from cell "empty"
			self.board[y-1][x] = movedPiece
		elif ((piece.color == "black") and ((y + 1) < 8) and (self.getPiece(x, y + 1).color == "")):
			#TODO: move "down" board
			print ''
		else:
			print "You tried to move forward a non-existent piece! (or moving forward is illegal)"
		return

	def moveL(self, piece):
		#TODO: move a piece forward-left
		return

	def moveR(self, piece):
		#TODO: move a piece forward-right
		return

	def printBoard(self):
		for i in range(self.height):
			for j in range(self.width):
				if game.board[i][j].color == "black":
					print 'B',
				elif game.board[i][j].color == "white":
					print 'W',
				else:
					print '.',
			print ''



class Piece(object):

	#This class will obviously have more private variables and methods. Still trying to figure out
	#	logistics and possible heuristics for part 2 :/
	color = ""
	xpos = 0
	ypos = 0
	value = 0

	def __init__(self, color, x, y):
		self.color = color
		self.xpos = x
		self.ypos = y

	def copy(self, other):
		self.color = other.color
		self.xpos = other.xpos
		self.ypos = other.ypos

	def evalValue(self):
		#TODO: write function(s) to determine the next favorable piece to move
		return

	#feel free to add more stuff idk




'''Main function routine'''
game = Game()
game.printBoard()
print '\n\nAfter moving one piece forward...'
tempPiece = game.getPiece(6,6)
game.moveF(tempPiece)
game.printBoard()
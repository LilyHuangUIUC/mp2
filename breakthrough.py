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

	def getPiece(self, col, row):
		# (0,0) = piece at top-left corner
		# (0,7) = piece at bottom-left corner
		# (7,0) = piece at top-right corner
		#an FYI, this function can also return an EMPTY cell (i.e. a "" piece)
		#	make sure above function caller checks for this
		i = row
		j = col
		return self.board[i][j]

	def checkF(self, piece):
		#check the spot in front of given piece (with respect to that piece)
		#returns either a color, "" (empty spot), or INV (invalid spot)
		x = piece.xpos
		y = piece.ypos
		if((piece.color == "white") and ((y - 1) >= 0)):
			return self.getPiece(x, y - 1).color
		elif ((piece.color == "black") and ((y + 1) < 8)):
			return self.getPiece(x, y + 1).color
		else:
			return "INV"	#we tried to access a cell outside the board
		return

	def moveF(self, piece):
		#move a piece forward.
		#obviously, don't have to worry about "taking over" other pieces as 
		#	we are ONLY moving straight-forward
		x = piece.xpos
		y = piece.ypos
		if(piece.color == "white" and self.checkF(piece) == ""):
			#moving "up" board onto empty cell
			movedPiece = copy.deepcopy(self.getPiece(x, y))
			self.board[y][x] = Piece("", x, y)	#make this moved from cell "empty"
			self.board[y-1][x] = movedPiece
			movedPiece.setY(y-1)
		elif (piece.color == "black" and self.checkF(piece) == ""):
			#moving "down" board onto empty cell
			movedPiece = copy.deepcopy(self.getPiece(x, y))
			self.board[y][x] = Piece("", x, y)	#make this moved from cell "empty"
			self.board[y+1][x] = movedPiece
			movedPiece.setY(y+1)
		elif (self.checkF(piece) == "INV"):
			print "You tried to move forward a piece off the board or into another piece!"
		else:
			print "You tried to move forward a non-existent piece!"
		return

	def checkFL(self, piece):
		#check spot to the forward-left of a given piece (w/ respect to that piece)
		#returns either a color, "" (empty spot), or INV (invalid spot)
		x = piece.xpos
		y = piece.ypos
		if((piece.color == "white") and ((y - 1) >= 0) and (x - 1) >= 0):
			return self.getPiece(x - 1, y - 1).color
		elif ((piece.color == "black") and ((y + 1) < 8) and (x + 1) < 8):
			return self.getPiece(x + 1, y + 1).color
		else:
			return "INV"	#we tried to access a cell outside the board
		return

	def moveFL(self, piece):
		#TODO: move a piece forward-left
		#we also need to check whether if there's an opposing piece going into
		#	"FL", in which case we can still move and MAYBE update a value...?
		x = piece.xpos
		y = piece.ypos
		if(piece.color == "white" and self.checkFL(piece) == ""):
			#moving "up-left" onto empty cell
			movedPiece = copy.deepcopy(self.getPiece(x, y))
			self.board[y][x] = Piece("", x, y)	#make this moved from cell "empty"
			self.board[y-1][x-1] = movedPiece
			movedPiece.setXY(x-1, y-1)
		elif (piece.color == "white" and self.checkFL(piece) == "black"):
			#white OVERTAKES a black piece here, update a value maybe...?
			movedPiece = copy.deepcopy(self.getPiece(x, y))
			self.board[y][x] = Piece("", x, y)	#make this moved from cell "empty"
			self.board[y-1][x-1] = movedPiece	#the "black" piece here will be gone
			movedPiece.setXY(x-1, y-1)
			return
		elif (piece.color == "black" and self.checkFL(piece) == ""):
			#moving "down-right" onto empty cell
			movedPiece = copy.deepcopy(self.getPiece(x, y))
			self.board[y][x] = Piece("", x, y)	#make this moved from cell "empty"
			self.board[y+1][x+1] = movedPiece
			movedPiece.setXY(x+1, y+1)
		elif (piece.color == "black" and self.checkFL(piece) == "white"):
			#black OVERTAKES a white piece here, update a value maybe...?
			movedPiece = copy.deepcopy(self.getPiece(x, y))
			self.board[y][x] = Piece("", x, y)	#make this moved from cell "empty"
			self.board[y+1][x+1] = movedPiece	#the "white" piece here will be gone
			movedPiece.setXY(x+1, y+1)
			return
		elif (self.checkF(piece) == "INV"):
			print "You tried to move forward-left a piece off the board or into a friendly piece!"
		else:
			print "You tried to move forward-left a non-existent piece!"
		return

	def checkFR(self, piece):
		#check spot to the forward-right of a given piece (w/ respect to that piece)
		#returns either a color, "" (empty spot), or INV (invalid spot)
		x = piece.xpos
		y = piece.ypos
		if((piece.color == "white") and ((y - 1) >= 0) and (x + 1) < 8):
			return self.getPiece(x + 1, y - 1).color
		elif ((piece.color == "black") and ((y + 1) < 8) and (x - 1) >= 0):
			return self.getPiece(x - 1, y + 1).color
		else:
			return "INV"	#we tried to access a cell outside the board
		return

	def moveFR(self, piece):
		#TODO: move a piece forward-left
		#we also need to check whether if there's an opposing piece going into
		#	"FR", in which case we can still move and MAYBE update a value...?
		x = piece.xpos
		y = piece.ypos
		if(piece.color == "white" and self.checkFL(piece) == ""):
			#moving "up-right" onto empty cell
			movedPiece = copy.deepcopy(self.getPiece(x, y))
			self.board[y][x] = Piece("", x, y)	#make this moved from cell "empty"
			self.board[y-1][x+1] = movedPiece
			movedPiece.setXY(x+1, y-1)
		elif (piece.color == "white" and self.checkFL(piece) == "black"):
			#white OVERTAKES a black piece here, update a value maybe...?
			movedPiece = copy.deepcopy(self.getPiece(x, y))
			self.board[y][x] = Piece("", x, y)	#make this moved from cell "empty"
			self.board[y-1][x+1] = movedPiece	#the "black" piece here will be gone
			movedPiece.setXY(x+1, y-1)
			return
		elif (piece.color == "black" and self.checkFL(piece) == ""):
			#moving "down-left" onto empty cell
			movedPiece = copy.deepcopy(self.getPiece(x, y))
			self.board[y][x] = Piece("", x, y)	#make this moved from cell "empty"
			self.board[y+1][x-1] = movedPiece
			movedPiece.setXY(x-1, y+1)
		elif (piece.color == "black" and self.checkFL(piece) == "white"):
			#black OVERTAKES a white piece here, update a value maybe...?
			movedPiece = copy.deepcopy(self.getPiece(x, y))
			self.board[y][x] = Piece("", x, y)	#make this moved from cell "empty"
			self.board[y+1][x-1] = movedPiece	#the "white" piece here will be gone
			movedPiece.setXY(x-1, y+1)
			return
		elif (self.checkF(piece) == "INV"):
			print "You tried to move forward-right a piece off the board or into a friendly piece!"
		else:
			print "You tried to move forward-right a non-existent piece!"
		return



	'''*******the rest of these "check" location functions may/may not be needed, but i'll write them for now****'''

	def checkL(self, piece):
		x = piece.xpos
		y = piece.ypos
		if((piece.color == "white") and (x - 1) >= 0):
			return self.getPiece(x - 1, y).color
		elif ((piece.color == "black") and (x + 1) < 8):
			return self.getPiece(x + 1, y).color
		else:
			return "INV"	#we tried to access a cell outside the board
		return

	def checkR(self, piece):
		x = piece.xpos
		y = piece.ypos
		if((piece.color == "white") and (x + 1) < 8):
			return self.getPiece(x + 1, y).color
		elif ((piece.color == "black") and (x - 1) >= 0):
			return self.getPiece(x - 1, y).color
		else:
			return "INV"	#we tried to access a cell outside the board
		return

	def checkB(self, piece):
		x = piece.xpos
		y = piece.ypos
		if((piece.color == "white") and ((y + 1) < 8)):
			return self.getPiece(x, y + 1).color
		elif ((piece.color == "black") and ((y - 1) >= 0)):
			return self.getPiece(x, y - 1).color
		else:
			return "INV"	#we tried to access a cell outside the board
		return

	def checkBL(self, piece):
		x = piece.xpos
		y = piece.ypos
		if((piece.color == "white") and ((y + 1) < 8) and (x - 1) >= 0):
			return self.getPiece(x + 1, y - 1).color
		elif ((piece.color == "black") and ((y - 1) >= 0) and (x + 1) < 8):
			return self.getPiece(x - 1, y + 1).color
		else:
			return "INV"	#we tried to access a cell outside the board
		return

	def checkBR(self, piece):
		x = piece.xpos
		y = piece.ypos
		if((piece.color == "white") and ((y + 1) < 8) and (x + 1) < 8):
			return self.getPiece(x + 1, y - 1).color
		elif ((piece.color == "black") and ((y - 1) >= 0) and (x - 1) >= 0):
			return self.getPiece(x - 1, y + 1).color
		else:
			return "INV"	#we tried to access a cell outside the board
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
			print ''	#just for a newline



class Piece(object):

	#This class will probably have more private variables and methods. Still trying to figure out
	#	logistics and possible heuristics for part 2 :/
	color = ""
	xpos = 0
	ypos = 0
	eaten = 0	#some value to keep track of number of opposing pieces "taken"
	value = 0

	def __init__(self, color, x, y):
		#color = "" ---> a board cell with an empty piece
		#color = "white" ---> a board cell with a white piece
		#color = "black" ---> a board cell with a black piece
		self.color = color
		self.xpos = x
		self.ypos = y

	def setXY(self, x, y):
		self.xpos = x
		self.ypos = y

	def setX(self, x):
		self.xpos = x

	def setY(self, y):
		self.ypos = y


	def evalValue(self):
		#TODO: write function(s) to determine the next favorable piece to move
		return

	#feel free to add more stuff idk




'''Main function routine'''
game = Game()
game.printBoard()
print '\n\nAfter moving one piece forward-left...'
tempPiece = game.getPiece(6,6)
game.moveFL(tempPiece)
game.printBoard()

print '\n\nAfter moving one piece forward-left...'
tempPiece = game.getPiece(5,5)
game.moveFL(tempPiece)
game.printBoard()

print '\n\nAfter moving one piece forward-left...'
tempPiece = game.getPiece(4,4)
game.moveFL(tempPiece)
game.printBoard()

print '\n\nAfter moving one piece forward-left...'
tempPiece = game.getPiece(3,3)
game.moveFL(tempPiece)
game.printBoard()

print '\n\nAfter moving one piece forward-left...'
tempPiece = game.getPiece(2,2)
game.moveFL(tempPiece)
game.printBoard()

print '\n\nAfter moving one piece forward-left...'
tempPiece = game.getPiece(1,1)
game.moveFL(tempPiece)
game.printBoard()
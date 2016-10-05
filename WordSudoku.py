import numpy as np
import heapq
import timeit


start = timeit.default_timer()
'''...................................read sudoku initial grid.................................'''
with open('grid2.txt') as f:
	c = []
	while True:
		p = f.read(1)
		if not p:
			break
		if not p =='\n':
			c.append(p)
		

#print(len(c))
grid = np.array(c).reshape(9,9)
#print(gridArray)



'''....................................read word bank...........................................'''
bank = open('wordbank2.txt').read().split('\n')





'''....................................check constrain...................................'''
def CheckConstrain(grid):
	unit = []
	for i in range(9):
		unit.append(grid[i,:])
		unit.append(grid[:,i])
	for m in [0,3,6]:
		for n in [0,3,6]:
			unit.append(grid[m:m+3,n:n+3].reshape(1,9))

	for item in unit:
		duplicate = CheckDuplicate(item)
		if duplicate:
			return 1
	return 0


def CheckDuplicate(item):
	for i in range(len(item)):
		for j in range(i+1, len(item)):
			if item[i] == item[j] and not item[i] == '_':
				return 1
	return 0


'''..................................legal value order.........................................'''
def LegalValue(grid, word): 
# Return ordered legal pos & direction of a word. "Legal" means the word is within the 9x9 grid, and does not 
# conflict with letters in grid. But for now we do not check the no duplication constrain.
# Value is in the form of (direction, position). eg. ('V',(3,2)) means vertical, first letter position(3,2) 
# Values are maintaned in a priority queue. They are ordered by how much they match to current grid.
	value_priority = []
	Max = 10 - len(word)
	# vertical assignment
	for i in range(Max):
		for j in range(9):
			array = grid[i:i+len(word),j] # a section of the grid that the word will overlap with
			match = MatchDegree(array,word) # return the match degree
			if not match == -1:
				pos = (i,j)
				value = ('V', pos)
				heapq.heappush(value_priority,(match,value)) #priority queue
	# horizontal assignment
	for i in range(9):
		for j in range(Max):
			array = grid[i,j:j+len(word)]
			match = MatchDegree(array,word)
			if not match == -1:
				pos = (i,j)
				value = ('H',pos)
				heapq.heappush(value_priority,(match,value))

	order_domain_values = []
	while value_priority:
		order_domain_values.append(heapq.heappop(value_priority))
	
	return order_domain_values # most matched value before less matched values


def MatchDegree(array,word): # compare a section of the grid and the word. Count # of the same letters
	match = 9
	for i in range(len(array)):
		if array[i] == word[i]:
			match -= 1
		if not array[i] == word[i]:
			if not array[i] =='_':
				return -1
	return match




'''............................................assign value..................................................'''
def AssignWord(grid, word, value): # fill the word into the grid by certain position and direction
	direction, (x,y) = value
	if direction == 'V':
		grid[x:x+len(word),y] = [letter for letter in word]
	if direction == 'H':
		grid[x,y:y+len(word)] = [letter for letter in word]

	return grid



'''......................................Select Unassigned Variable.........................................'''
def SelectWord(bank): #Select the longest word. Attempt to select the most constrained variable
	while(bank):
		longest = bank[0]
		length = len(longest)
		for word in bank:
			if len(word) > length:
				length = len(word)
				longest = word
		return longest



'''.......................................Recursive Backtracking.............................................'''
def SudokuSearch(grid,bank): # lecture notes 7, slide 19
	if complete(grid):
		return grid

	word = SelectWord(bank)
	order_domain_values = LegalValue(grid,word)

	for item in order_domain_values:
		match, value = item
		grid_backup = grid.copy()
		grid_attempt = grid.copy()
		grid_attempt = AssignWord(grid_attempt,word,value)
		if not CheckConstrain(grid_attempt):
			grid = grid_attempt.copy() #add value to variable
			bank.remove(word) #print the process of assigning words
			print(word,value)
			result = SudokuSearch(grid,bank)
			if not result == -1:
				return result
			grid = grid_backup.copy() #remove value from variable
			bank.append(word)
	return -1


def complete(grid): # the grid is full
	for i in range(9):
		for j in range(9):
			if grid[i][j] == '_':
				return 0
	return 1



result = SudokuSearch(grid,bank)
print(result)


stop = timeit.default_timer() #run time

print (stop-start)







import random as rnd
import numpy as np
from anytree import Node, RenderTree, PostOrderIter, LevelOrderGroupIter
import variables as v
# returns row and column based on position of hex board
# translates hex position into array index
def getRowCol(pos):

    try:
        row = [1, 12, 23, 34, 45, 56, 67, 78, 89, 100, 111].index(pos)+1
        col = 'A'#ascii #65
        return [row, col]
    except ValueError:
        pass

    try:
        row = [2, 13, 24, 35, 46, 57, 68, 79, 90, 101, 112].index(pos)+1
        col = 'B' #66
        return [row, col]
    except ValueError:
        pass

    try:
        row = [3, 14, 25, 36, 47, 58, 69, 80, 91, 102, 113].index(pos)+1
        col = 'C' #67
        return [row, col]
    except ValueError:
        pass

    try:
        row = [4, 15, 26, 37, 48, 59, 70, 81, 92, 103, 114].index(pos)+1
        col = 'D' #68
        return [row, col]
    except ValueError:
        pass

    try:
        row = [5, 16, 27, 38, 49, 60, 71, 82, 93, 104, 115].index(pos)+1
        col = 'E' #69
        return [row, col]
    except ValueError:
        pass

    try:
        row = [6, 17, 28, 39, 50, 61, 72, 83, 94, 105, 116].index(pos)+1
        col = 'F' #70
        return [row, col]
    except ValueError:
        pass

    try:
        row = [7, 18, 29, 40, 51, 62, 73, 84, 95, 106, 117].index(pos)+1
        col = 'G' #71
        return [row, col]
    except ValueError:
        pass

    try:
        row = [8, 19, 30, 41, 52, 63, 74, 85, 96, 107, 118].index(pos)+1
        col = 'H' #72
        return [row, col]
    except ValueError:
        pass

    try:
        row = [9, 20, 31, 42, 53, 64, 75, 86, 97, 108, 119].index(pos)+1
        col = 'I' #73
        return [row, col]
    except ValueError:
        pass

    try:
        row = [10, 21, 32, 43, 54, 65, 76, 87, 98, 109, 120].index(pos)+1
        col = 'J' #74
        return [row, col]
    except ValueError:
        pass

    try:
        # Row decides the value of the number for ex. f11: row = 11
        row = [11, 22, 33, 44, 55, 66, 77, 88, 99, 110, 121].index(pos)+1
        col = 'K' #75
        return [row, col]
    except ValueError:
        pass

    return [99, 'X'] # return invalid piece index, board position


class HashInput:
  def __init__(self, zobristKey, DEPTH, flag, evaluation, oldEntry, move):
    self.zobrist = zobristKey
    self.DEPTH = DEPTH
    self.flag = flag
    self.eval = evaluation
    self.oldEntry = oldEntry
    self.move = move


def cube_to_axial(cube):
    q = cube[:, 0]
    r = cube[:, 2]
    return (q, r)

def axial_to_cube(hexchoord):
    z = hexchoord[0]
    x = hexchoord[1]
    y = -x-z
    return (x, y, z)

def cube_distance(a, b):
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]), abs(a[2] - b[2]))


def hex2Cube(position):
	posV = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K'].index(position[0])+1
	x = posV - 6
	z = position[1] - (position[1] - (6-posV))
	y = -x-z

	return (x, y, z)
# Check if the position is under attack give 1 point if there is no piece there and 5 if there is an opponents piece there
def attack(position, pieceList):
	pieceList_map = np.array(list(pieceList))

	if position[0] in pieceList[:, 0] \
	and position[1] in pieceList[:, 1] \
	and position[2] in pieceList[:, 2]:
		if sum(position) == 0:
			return True

	return False


#print(attack([0,  4, -4], v.pieceList_map))

def validPos(pos):
	if ((pos[0] or pos[1] or pos[2]) > 5 or (pos[0] or pos[1] or pos[2]) < -5):
		return False

	return sum(pos) == 0

def eval():
	return 0

# # Move is valid [[0, 0, 0], [0, -1, 1]]
def makeMove(move, board):
	#print('make: ', move)
	fromA = tuple(move[0])
	toB = tuple(move[1])
	zobristKey = board

	if not validMove(move):
		return [zobristKey, '', False]

	v.pieceList_mapCopy[toB] = [v.pieceList_mapCopy[fromA][0], v.pieceList_mapCopy[fromA][1], rnd.getrandbits(64)]
	historyZobrist = v.pieceList_mapCopy[fromA][2]
	# Update Zobrist key board
	zobristKey ^= v.pieceList_mapCopy[fromA][2]
	zobristKey ^= v.pieceList_mapCopy[toB][2]
	del v.pieceList_mapCopy[fromA]
	#print('made: ', move)
	return [zobristKey, historyZobrist, True]

def undoMove(move, board, historyZobrist):

	fromA = tuple(move[0])
	toB = tuple(move[1])
	zobristKey = board
	#print('undo:', move)
	v.pieceList_mapCopy[fromA] = [v.pieceList_mapCopy[toB][0], v.pieceList_mapCopy[toB][1], historyZobrist]

	# Update Zobrist key board
	zobristKey ^= v.pieceList_mapCopy[fromA][2]
	zobristKey ^= v.pieceList_mapCopy[toB][2]
	del v.pieceList_mapCopy[toB]

	return zobristKey

# Check if a move is valid [[0, 0, 0], [0, -1, 1]]
def validMove(move):
	#print('Valid move', move)
	pieceList_map2 = np.array(list(v.pieceList_mapCopy))
	# Move is not on the same line neither vertically, horizontally nor diagonally
	if not( move[0][0] == move[1][0] or move[0][1] == move[1][1] or move[0][2] == move[1][2]):
		# print('off track')
		return False

		# There is no piece on the from location and it is this your own team
	elif not move[0] in v.pieceList_mapCopy:
		# print('no piece')
		return False

	# There is a piece on the to location and it is this your own team
	elif move[1] in v.pieceList_mapCopy and \
	(v.pieceList_mapCopy[move[0]][1] in ['n', 'm', 'p'] \
	or v.pieceList_mapCopy[move[0]][1] in ['N', 'M', 'P'] ):
		# print('own piece attacked')
		return False

	# Starting location false coordinates
	elif not (validPos(move[0]) or validPos(move[1])) :
		# print('start or end is not on grid, false coords')
		return False

	# F6 (0, 0, 0) is between the two locations
	elif move[0][0] == move[1][0] and move[1][0] == 0 and \
	0 in (range(move[0][1], move[1][1]) or range(move[1][1], move[0][1])) and \
	0 in (range(move[0][2], move[1][2]) or range(move[1][2], move[0][2])): #up or down 
		#print('f61')
		return False
	elif 0 in (range(move[0][0], move[1][0]) or range(move[1][0], move[0][0])) and \
	move[0][1] == move[1][1] and move[1][1] == 0 and \
	0 in (range(move[0][2], move[1][2]) or range(move[1][2], move[0][2])): # up or down diagonal
		#print('f62')
		return False
	elif 0 in (range(move[0][0], move[1][0]) or range(move[1][0], move[0][0])) and \
	0 in (range(move[0][1], move[1][1]) or range(move[1][1], move[0][1])) and \
	move[0][2] == move[1][2] and move[1][2] == 0:
		#print('f63')
		return False

	# There is a piece between the to and from position
	elif not ((move[0][0] == move[1][0] and move[0][1] > move[1][1]) or (move[0][0] == move[1][0] and move[0][1] < move[1][1]) or (move[0][1] == move[1][1] and move[0][0] > move[1][0])  or ( move[0][1] == move[1][1] and move[0][0] < move[1][0])  or (move[0][2] == move[1][2] and move[0][0] < move[1][0])  or (move[0][2] == move[1][2]and move[0][0] > move[1][0]) ):
		# print('Same direction')	
		return False


	# There is a piece between the to and from position
	elif (move[0][0] == move[1][0] and move[0][1] > move[1][1]):
		new = np.array(move[0])
		for i in range(move[0][1] - move[1][1]):
			new -= SW
			new = tuple(new)
			if new in list(v.pieceList_mapCopy):
				return False

	# There is a piece between the to and from position
	elif (move[0][0] == move[1][0] and move[0][1] < move[1][1]):
		new = np.array(move[0])
		for i in range(move[1][1] - move[0][1]):
			new += SW
			new = tuple(new)
			if new in list(v.pieceList_mapCopy):
				return False

	# There is a piece between the to and from position
	elif (move[0][1] == move[1][1] and move[0][0] > move[1][0]):
		new = np.array(move[0])
		for i in range(move[0][0] - move[1][0]):
			new += NW
			new = tuple(new)
			if new in list(v.pieceList_mapCopy):
				return False

	# There is a piece between the to and from position
	elif (move[0][1] == move[1][1] and move[0][0] < move[1][0]):
		new = np.array(move[0])
		for i in range(move[1][0] - move[0][0]):
			new -= NW
			new = tuple(new)
			if new in list(v.pieceList_mapCopy):
				return False

	# There is a piece between the to and from position
	elif (move[0][2] == move[1][2] and move[0][1] > move[1][1]):
		new = np.array(move[0])
		for i in range(move[0][1] - move[1][1]):
			new += E
			new = tuple(new)
			if new in list(v.pieceList_mapCopy):
				return False

	# There is a piece between the to and from position
	elif (move[0][2] == move[1][2] and move[0][1] < move[1][1]):
		new = np.array(move[0])
		for i in range(move[1][1] - move[0][1]):
			new -= E
			new = tuple(new)
			if new in list(v.pieceList_mapCopy):
				return False

	return True

gameover = False
winningScore = 100
WIN  = 1000
current_DEPTH = 0

def iterativeDeepening():
    while haveTime():
        eval = alphaBeta(current_DEPTH, -200000, 200000)
        current_DEPTH += 1


def haveTime():
    return True

def cube_distance(a, b):
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]), abs(a[2] - b[2]))

def miniMax(board, DEPTH):
	nodes = 0
	depth = DEPTH
	if depth == 0: return 1 #root

	moves = createAllMoves(depth)

	for key, move in moves:
		for m in move:
			mov = [key[1], tuple(m)]
			makeMove(mov, board)
			nodes += miniMax(board, depth)
			undoMove(mov, board, historyZobrist)
		depth -= 1

	return nodes


#principal variation search (fail-soft version)
def alphaBeta(DEPTH, alpha, beta):
        #move bestmove, current
        if (gameOver or DEPTH <= 0):
        	return winningScore or eval()
        m = firstMove
        makeMove(m)
        current = -alphabeta(DEPTH - 1, -beta, -alpha)
        unmakeMove(m)
        for m in allMoves():
            makeMove(m)
            score = -alphabeta(DEPTH - 1, -alpha-1, -alpha)
            if (score > alpha and score < beta):
                score = -alphabeta(DEPTH - 1, -beta, -alpha)
            unmakeMove(m)
            if (score >= current):
                current = score
                bestmove = m
                if (score >= alpha): alpha = score
                if (score >= beta): break
        
        return current
    

#(10, (0, 3, -3)): [(-1, 3, -2), (-2, 3, -1), (-3, 3, 0), (-4, 3, 1), (-5, 3, 2), (0, 2, -2), (0, 1, -1), (0, 0, 0), (1, 2, -3), (2, 1, -3), (3, 0, -3), (4, -1, -3), (5, -2, -3)]
def createAllMoves(depth):

	root, moves = createMoves2(depth, v.pieceList_mapCopy)
	#return moves

	#print(root.children)
	#r = Node(('DHoehdoin'), parent=root)


	for i in range(depth+1):
		# Check for all the next moves
		for piece in v.pieceList_mapCopy:
			if (i, piece) in moves:
				for move in moves[(i, piece)]:
					if validMove([piece, move]):
						for node in PostOrderIter(root):
							if node.name == piece:
								Node(move, parent=node)
								#print(node.name==piece, move, piece)
	print(RenderTree(root))
	return moves

def createMoves(depth, pieceList):
	#  Walk in a direction until you hit someone
	pieces = pieceList
	plyList = {}
	moves = {}
	Total = 0
	zobristInit = boardInit()
	DEPTH = depth
	moves = []
	piecesl = []
	for piece in pieces:
		#print(piece, 'printed')
		plyList[piece] = 0
		piecesl = [piece]
		clash = False
		moves[(DEPTH, piece)] = []

		for direction in range(len(ALL_DIRECTIONS)):
			new = np.array(piece)
			
			for j in range(-5, 5):

				new += ALL_DIRECTIONS[direction]
				move = [piece, tuple(new)]

				if tuple(new) in v.hexboard_map and v.hexboard_map[tuple(new)] == -1 \
				or not tuple(new) in v.hexboard_map:
					#print(' not accessible', move)
					break

				if (new[0] | new[1] | new[2]) > 5 or (new[0] | new[1] | new[2]) < -5:
					#print('Off grid', move)
					break

				m = makeMove(move, zobristInit)
				if m[2]:
					moves[(DEPTH, piece)] += [move[1]]
					undoMove(move, m[0], m[1])

					plyList[piece] += 1
					Total += 1


	# for p in plyList:
	# 	print(p, plyList[p])
	print('Total moves at DEPTH: ', DEPTH, ': ', Total)
	return moves


def drawBoard():
	col = 'A'
	row = 1
	strs = '' # boardString, hex format

	for pos in range(1, 121):

		row, col = getRowCol(pos) #convert to [A, 1] format
		x, y, z = hex2Cube([col, row])

		if validPos((x, y, z)):
			if (x, y, z) in v.pieceList_map:
				print((col, row), (x, y, z))
				if v.hexboard_map[(x, y, z)] != -1:
				    strs += ' ' + str(v.pieceList_map[(x, y, z)][1])
				elif v.hexboard_map[(x, y, z)] == -1:
				    strs += ' '  #str(board[pos])
			else:
				if v.hexboard_map[(x, y, z)] != -1:
				    strs += ' ' + '-'
				elif v.hexboard_map[(x, y, z)] == -1:
				    strs += '  ' #str(board[pos])

			# Next line, use for creating a board
			if pos > 0 and pos % 11 == 0:
			    strs += '\n'
			    if pos % 2 == 0:
			        strs += ''


	return '\n' + strs

# initialize board
def boardInit():
	zobristKey = 0
	distList = []
	for key, value in v.pieceList_map.items():
		distList.append(key)

	for pos in range(1, 121):
		row, col = getRowCol(pos) #convert to [A, 1] format
		x, y, z = hex2Cube([col, row])
		if v.hexboard_map[(x, y, z)] != -1:
			zobristKey ^= v.hexboard_map[(x, y, z)]
			try:
				distList.index((x, y, z)) # Check if there is a piece at this location
				zobristKey ^= v.pieceList_map[(x, y, z)][2]
			except ValueError: ''
	return zobristKey

print(boardInit())


def createMoves2(depth, pieceList):
	#  Walk in a direction until you hit someone
	pieces = pieceList
	plyList = {}
	moves = {}
	Total = 0
	zobristInit = boardInit()
	DEPTH = depth
	moves = {}
	piecesl = []


	root = Node(str(DEPTH))

	for piece in pieces:
		#print(piece, 'printed')
		plyList[piece] = 0
		piecesl = [piece]
		moves[(DEPTH, piece)] = []
		clash = False
		child = Node(piece, parent=root)

		for direction in range(len(ALL_DIRECTIONS)):
			n


						# temp, v.pieceList_mapCopy[move] = v.pieceList_mapCopy[piece], v.pieceList_mapCopy[piece]
						# del v.pieceList_mapCopy[piece]
						#print('hiero')
						#child = Node(move, parent=piece)
						#moves.update(createMoves(i+1, v.pieceList_mapCopy)) # create moves for new position
						#v.pieceList_mapCopy[piece] = temp
						#del v.pieceList_mapCopy[move]
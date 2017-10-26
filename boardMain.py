import random as rnd
import numpy as np
from anytree import Node, RenderTree


# These are the vectors for moving from any hex to one of its neighbors.
SE = np.array((1, 0, -1))
SW = np.array((0, 1, -1))
W = np.array((-1, 1, 0))
NW = np.array((-1, 0, 1))
NE = np.array((0, -1, 1))
E = np.array((1, -1, 0))
ALL_DIRECTIONS = np.array([NW, NE, E, SE, SW, W, ])
cube_diagonals = np.array([
   (+2, -1, -1), (+1, +1, -2), (-1, +2, -1), 
   (-2, +1, +1), (-1, -1, +2), (+1, -2, +1)
])
DEPTH = 0

zobristKey = 1 # Zobrist key of board position
DEPTH = 0 # the ply in which you perform the search
flag = 0 # exact, alhpa, beta, determines cut off
evaluation = 0 # States if the side to move is ahead
oldEntry = 1 # Entry in table that has been obtained on lower ply
move = [] # The move that was best on a certain DEPTH
historyHash = []
historyZobrist = 1 # store zobrist of from location
side = 1 # 1 = black moves, 0 = white moves


# cube board
hexboard_map = {
(-5, 10, -5): -1,
(-5, 9, -4): -1,
(-5, 8, -3): -1,
(-5, 7, -2): -1,
(-5, 6, -1): -1,
(-5, 5, 0): 1939212919950939759,
(-5, 4, 1): 9849431805437009732,
(-5, 3, 2): 16162666918917919806,
(-5, 2, 3): 15276516314310390362,
(-5, 1, 4): 11642453785499409731,
(-5, 0, 5): 4198843929353293072,

(-4, 9, -5): -1,
(-4, 8, -4): -1,
(-4, 7, -3): -1,
(-4, 6, -2): -1,
(-4, 5, -1): 242836734077330547,
(-4, 4, 0): 1027919702168188979,
(-4, 3, 1): 16832440912975894468,
(-4, 2, 2): 17340713814242594028,
(-4, 1, 3): 16266090026993502319,
(-4, 0, 4): 7984883234528157998,
(-4, -1, 5): 40694595421736207,

(-3, 8, -5): -1,
(-3, 7, -4): -1,
(-3, 6, -3): -1,
(-3, 5, -2): 12606065518542938582,
(-3, 4, -1): 139336708204130549,
(-3, 3, 0): 9404967577669660609,
(-3, 2, 1): 16988572083252292303,
(-3, 1, 2): 7774238338669335086,
(-3, 0, 3): 15158629369172322486,
(-3, -1, 4): 16361351586279929792,
(-3, -2, 5): 15132990715107860610,

(-2, 7, -5): -1,
(-2, 6, -4): -1,
(-2, 5, -3): 5267051858285417275,
(-2, 4, -2): 6790307694184382222,
(-2, 3, -1): 3573834257037273296,
(-2, 2, 0): 5286160300075179554,
(-2, 1, 1): 10897662397012006653,
(-2, 0, 2): 17483553982907062074,
(-2, -1, 3): 6324615498667232688,
(-2, -2, 4): 3214998845050975716,
(-2, -3, 5): 9587047821109070005,

(-1, 6, -5): -1,
(-1, 5, -4): 144597867867711702,
(-1, 4, -3): 17775915297188647818,
(-1, 3, -2): 18407867710085699471,
(-1, 2, -1): 10653868923730995775,
(-1, 1, 0): 4101508452747031293,
(-1, 0, 1): 4432349630158972496,
(-1, -1, 2): 6428893941102858473,
(-1, -2, 3): 5262733008685202359,
(-1, -3, 4): 1566494270541933283,
(-1, -4, 5): 9731098770160265163,

(0, 5, -5): 2448042715754671234,
(0, 4, -4): 10120822579704798707,
(0, 3, -3): 18112980892344717096,
(0, 2, -2): 6176237247625849847,
(0, 1, -1): 17653286343034920267,
(0, 0, 0): 9453218997835932307,
(0, -1, 1): 13313380641917178378,
(0, -2, 2): 3300729307248399927,
(0, -3, 3): 1503336893889795583,
(0, -4, 4): 10060660257644807637,
(0, -5, 5): 2613961411735854838,

(1, 4, -5): 13476510822332751603,
(1, 3, -4): 14862051557182589828,
(1, 2, -3): 4994050721206873361,
(1, 1, -2): 1533047034780867359,
(1, 0, -1): 14733174309712718937,
(1, -1, 0): 13288936609690794407,
(1, -2, 1): 8654508882559949035,
(1, -3, 2): 18071121815839094851,
(1, -4, 3): 14290800167692211014,
(1, -5, 4): 15521623660326241119,
(1, -6, 5): -1,

(2, 3, -5): 6336409208809923494,
(2, 2, -4): 15711127134202039181,
(2, 1, -3): 13621517375642790498,
(2, 0, -2): 7536982841581896974,
(2, -1, -1): 17265457799223545964,
(2, -2, 0): 1375358603569454382,
(2, -3, 1): 10724534189979383858,
(2, -4, 2): 16134249891398683417,
(2, -5, 3): 11359358801631150336,
(2, -6, 4): -1,
(2, -7, 5): -1,

(3, 2, -5): 4120461599787512707,
(3, 1, -4): 6432106195970801773,
(3, 0, -3): 9163956974091406101,
(3, -1, -2): 7702706718074166436,
(3, -2, -1): 13618073712606537975,
(3, -3, 0): 972414462113362012,
(3, -4, 1): 15348376841733596592,
(3, -5, 2): 16267665463287930254,
(3, -6, 3): -1,
(3, -7, 4): -1,
(3, -8, 5): -1,

(4, 1, -5): 7330334617727317686,
(4, 0, -4): 15816374442629084416,
(4, -1, -3): 9789732663738897482,
(4, -2, -2): 612255692993768337,
(4, -3, -1): 13939161138629257191,
(4, -4, 0): 592301583230350119,
(4, -5, 1): 17968089013567309362,
(4, -6, 2): -1,
(4, -7, 3): -1,
(4, -8, 4): -1,
(4, -9, 5): -1,

(5, 0, -5): 3135654740086792305,
(5, -1, -4): 8857702522973846636,
(5, -2, -3): 18295052659086930627,
(5, -3, -2): 11858234084313267846,
(5, -4, -1): 7355896468892986707,
(5, -5, 0): 14471375923077555854,
(5, -6, 1): -1,
(5, -7, 2): -1,
(5, -8, 3): -1,
(5, -9, 4): -1,
(5, -10, 5): -1}

pieceList_map = {
#b pieces
(0, 5, -5): [0, 'N', 7039324259174552899],
(-2, 5, -3): [-1, 'P', 2708738351447517863],
(-1, 4, -3): [1, 'M', 17276587691014336917],#
(0, 3, -3): [-1, 'P', 1811291666407332732],
(1, 4, -5): [1, 'M', 13326266845422094801],#
(1, 3, -4): [1, 'M', 1809515583972370874],
(-1, 5, -4): [1, 'M', 16240295312056102057],
(2, 3, -5): [-1, 'P', 1571580890494471027],
(0, 4, -4): [-1, 'P', 14017614727057677400],

# w pieces
(-2, -3, 5): [-1, 'm', 14917430532102944307],
(-1, -4, 5): [1, 'n', 3843109819342283363],#
(0, -5, 5): [0, 'p', 10807404499587620088], #
(0, -3, 3): [-1, 'm', 9592769839177490520],#
(-1, -3, 4): [1, 'p', 5554593599456045088],
(1, -5, 4): [1, 'p', 1938315421320155298],
(1, -4, 3): [1, 'p', 10195476464469860234],
(2, -5, 3): [-1, 'm', 12339900744325023683],
(0, -4, 4): [-1, 'm', 688889229393588896]#
}


pieceList_mapCopy = {
#b pieces
(0, 5, -5): [0, 'N', 7039324259174552899],
(-2, 5, -3): [-1, 'P', 2708738351447517863],
(-1, 4, -3): [1, 'M', 17276587691014336917],#
(0, 3, -3): [-1, 'P', 1811291666407332732],
(1, 4, -5): [1, 'M', 13326266845422094801],#
(1, 3, -4): [1, 'M', 1809515583972370874],
(-1, 5, -4): [1, 'M', 16240295312056102057],
(2, 3, -5): [-1, 'P', 1571580890494471027],
(0, 4, -4): [-1, 'P', 14017614727057677400],

# w pieces
(-2, -3, 5): [-1, 'm', 14917430532102944307],
(-1, -4, 5): [1, 'n', 3843109819342283363],#
(0, -5, 5): [0, 'p', 10807404499587620088], #
(0, -3, 3): [-1, 'm', 9592769839177490520],#
(-1, -3, 4): [1, 'p', 5554593599456045088],
(1, -5, 4): [1, 'p', 1938315421320155298],
(1, -4, 3): [1, 'p', 10195476464469860234],
(2, -5, 3): [-1, 'm', 12339900744325023683],
(0, -4, 4): [-1, 'm', 688889229393588896]#
}

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
def attack(position, pieceList_map):
	pieceList_map = np.array(list(pieceList_map))

	if position[0] in pieceList_map[:, 0] \
	and position[1] in pieceList_map[:, 1] \
	and position[2] in pieceList_map[:, 2]:
		if sum(position) == 0:
			return True

	return False


#print(attack([0,  4, -4], pieceList_map))

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

	pieceList_mapCopy[toB] = [pieceList_mapCopy[fromA][0], pieceList_mapCopy[fromA][1], rnd.getrandbits(64)]
	historyZobrist = pieceList_mapCopy[fromA][2]
	# Update Zobrist key board
	zobristKey ^= pieceList_mapCopy[fromA][2]
	zobristKey ^= pieceList_mapCopy[toB][2]
	del pieceList_mapCopy[fromA]
	#print('made: ', move)
	return [zobristKey, historyZobrist, True]

def undoMove(move, board, historyZobrist):

	fromA = tuple(move[0])
	toB = tuple(move[1])
	zobristKey = board
	#print('undo:', move)
	pieceList_mapCopy[fromA] = [pieceList_mapCopy[toB][0], pieceList_mapCopy[toB][1], historyZobrist]

	# Update Zobrist key board
	zobristKey ^= pieceList_mapCopy[fromA][2]
	zobristKey ^= pieceList_mapCopy[toB][2]
	del pieceList_mapCopy[toB]

	return zobristKey

# Check if a move is valid [[0, 0, 0], [0, -1, 1]]
def validMove(move):
	#print('Valid move', move)
	pieceList_map2 = np.array(list(pieceList_mapCopy))
	# Move is not on the same line neither vertically, horizontally nor diagonally
	if not( move[0][0] == move[1][0] or move[0][1] == move[1][1] or move[0][2] == move[1][2]):
		# print('off track')
		return False

		# There is no piece on the from location and it is this your own team
	elif not move[0] in pieceList_mapCopy:
		# print('no piece')
		return False

	# There is a piece on the to location and it is this your own team
	elif move[1] in pieceList_mapCopy and \
	(pieceList_mapCopy[move[0]][1] in ['n', 'm', 'p'] \
	or pieceList_mapCopy[move[0]][1] in ['N', 'M', 'P'] ):
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
			if new in list(pieceList_mapCopy):
				return False

	# There is a piece between the to and from position
	elif (move[0][0] == move[1][0] and move[0][1] < move[1][1]):
		new = np.array(move[0])
		for i in range(move[1][1] - move[0][1]):
			new += SW
			new = tuple(new)
			if new in list(pieceList_mapCopy):
				return False

	# There is a piece between the to and from position
	elif (move[0][1] == move[1][1] and move[0][0] > move[1][0]):
		new = np.array(move[0])
		for i in range(move[0][0] - move[1][0]):
			new += NW
			new = tuple(new)
			if new in list(pieceList_mapCopy):
				return False

	# There is a piece between the to and from position
	elif (move[0][1] == move[1][1] and move[0][0] < move[1][0]):
		new = np.array(move[0])
		for i in range(move[1][0] - move[0][0]):
			new -= NW
			new = tuple(new)
			if new in list(pieceList_mapCopy):
				return False

	# There is a piece between the to and from position
	elif (move[0][2] == move[1][2] and move[0][1] > move[1][1]):
		new = np.array(move[0])
		for i in range(move[0][1] - move[1][1]):
			new += E
			new = tuple(new)
			if new in list(pieceList_mapCopy):
				return False

	# There is a piece between the to and from position
	elif (move[0][2] == move[1][2] and move[0][1] < move[1][1]):
		new = np.array(move[0])
		for i in range(move[1][1] - move[0][1]):
			new -= E
			new = tuple(new)
			if new in list(pieceList_mapCopy):
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

	moves = createMoves(i, pieceList_mapCopy)

	for i in range(depth+1):

		# Check for all the next moves
		for piece in pieceList_mapCopy:
			if (i, piece) in moves:
				for move in moves[(i, piece)]:
					if validMove([piece, move]):
						temp, pieceList_mapCopy[move] = pieceList_mapCopy[piece], pieceList_mapCopy[piece]
						del pieceList_mapCopy[piece]
						#print('hiero')
						
						moves.update(createMoves(i+1, pieceList_mapCopy)) # create moves for new position
						pieceList_mapCopy[piece] = temp
						del pieceList_mapCopy[move]
	return moves

def createMoves(depth, pieceList):
	#  Walk in a direction until you hit someone
	pieces = pieceList
	plyList = {}
	moves = {}
	Total = 0
	zobristInit = boardInit()
	DEPTH = depth
	moves[DEPTH] = []
	piecesl = []
	for piece in pieces:
		#print(piece, 'printed')
		plyList[piece] = 0
		piecesl = [piece]
		clash = False

		for direction in range(len(ALL_DIRECTIONS)):
			new = np.array(piece)
			
			for j in range(-5, 5):

				new += ALL_DIRECTIONS[direction]
				move = [piece, tuple(new)]

				if tuple(new) in hexboard_map and hexboard_map[tuple(new)] == -1 \
				or not tuple(new) in hexboard_map:
					#print(' not accessible', move)
					break

				if (new[0] | new[1] | new[2]) > 5 or (new[0] | new[1] | new[2]) < -5:
					#print('Off grid', move)
					break

				m = makeMove(move, zobristInit)
				if m[2]:
					piecesl += [move[1]]
					undoMove(move, m[0], m[1])

					plyList[piece] += 1
					Total += 1
		moves[DEPTH] += [piecesl]


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
			if (x, y, z) in pieceList_map:
				print((col, row), (x, y, z))
				if hexboard_map[(x, y, z)] != -1:
				    strs += ' ' + str(pieceList_map[(x, y, z)][1])
				elif hexboard_map[(x, y, z)] == -1:
				    strs += ' '  #str(board[pos])
			else:
				if hexboard_map[(x, y, z)] != -1:
				    strs += ' ' + '-'
				elif hexboard_map[(x, y, z)] == -1:
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
	for key, value in pieceList_map.items():
		distList.append(key)

	for pos in range(1, 121):
		row, col = getRowCol(pos) #convert to [A, 1] format
		x, y, z = hex2Cube([col, row])
		if hexboard_map[(x, y, z)] != -1:
			zobristKey ^= hexboard_map[(x, y, z)]
			try:
				distList.index((x, y, z)) # Check if there is a piece at this location
				zobristKey ^= pieceList_map[(x, y, z)][2]
			except ValueError: ''
	return zobristKey

print(boardInit())
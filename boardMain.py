import random as rnd
import numpy as np


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
(0, 5, -5): [0, 'N', 7039324259174552899], # (-5, 5, 0):
(-2, 5, -3): [-1, 'P', 2708738351447517863],
(0, 4, -4): [-1, 'P', 14017614727057677400],
(-1, 4, -3): [1, 'M', 17276587691014336917],
(0, 3, -3): [-1, 'P', 1811291666407332732],
(1, 4, -5): [1, 'M', 13326266845422094801],
(1, 3, -4): [1, 'M', 1809515583972370874],
(-1, 5, -4): [1, 'M', 16240295312056102057],
(2, 3, -5): [-1, 'P', 1571580890494471027],

# w pieces
(-2, -3, 5): [-1, 'm', 14917430532102944307], #(5, -3, -2):
(-1, -4, 5): [1, 'n', 3843109819342283363],
(0, -5, 5): [0, 'p', 10807404499587620088],
(0, -4, 4): [-1, 'm', 688889229393588896],
(0, -3, 3): [-1, 'm', 9592769839177490520],
(-1, -3, 4): [1, 'p', 5554593599456045088],
(1, -5, 4): [1, 'p', 1938315421320155298],
(1, -4, 3): [1, 'p', 10195476464469860234],
(2, -5, 3): [-1, 'm', 12339900744325023683]
}

def hex2Cube(position):
	x = ord(position[0]) - ord('A')-5
	z = position[1]
	#exchange rate, convert everything to scale between -5 and 5
	if position[1] <= 6:
		z -= 6
	else:
		z -= 5
		
	y = -x-z
	return (x, y, z)
# Check if the position is under attack give 1 point if there is no piece there and 5 if there is an opponents piece there
def attack(position, pieceList_map):
	pieceList_map = np.array(list(pieceList_map))
	if position[0] in pieceList_map[:, 0] \
	and position[1] in pieceList_map[:, 1] \
	and position[2] in pieceList_map[:, 2]:
		return True

	return False


print(attack([0,  4, -4], pieceList_map))

def validPos(pos):
	return sum(pos) == 0

def drawboard2():
	draw = ''
	nextline = 1 
	for x in range(-6, 7):
		for y in range(-6, 7):
			if (x, y) in board:
				if (x, y) in pieceList:
					if pieceList[(x, y)][0] == -1:
				 		draw += '-'
					elif pieceList[(x, y)][0] == 1:
					 	draw += '+'
					else:
						draw += '='
				else:
					draw += '_'
			else:
				draw += ' '

			if nextline % 13 == 0:
				draw += '\n'

			nextline += 1

	print(draw)

def eval():
	return 0

def makeMove(move):
	pieceList_map[move[1]] = pieceList_map[move[0]]
	del pieceList_map[move[0]]
	# return 0

def unmakeMove(move):
	pieceList_map[move[0]] = pieceList_map[move[1]]
	del pieceList_map[move[1]]
	# return 0

# Check if a move is valid [[0, 0, 0], [0, -1, 1]]
def validMove(move):
	print(move)
	# Move is not on the same line neither vertically, horizontally nor diagonally
	if not( move[0][0] == move[1][0] or move[0][1] == move[1][1] or move[0][2] == move[1][2]):
		#print('off track')
		return False

	# There is a piece on the to location and it is this your own team
	elif move[1] in pieceList_map and \
	(pieceList_map[move[0]][1] in ['n', 'm', 'p'] \
	or pieceList_map[move[0]][1] in ['N', 'M', 'P'] ):
		#print('own piece attacked')
		return False

	# There is no piece on the from location and it is this your own team
	elif not move[0] in pieceList_map:
		#print('no piece')
		return False

	# Starting location false coordinates
	elif not (validPos(move[0]) or validPos(move[1])) :
		#print('start or end is not on grid, false coords')
		return False

	# F6 (0, 0, 0) is between the two locations
	elif move[0][0] == move[1][0] and move[1][0] == 0 and \
	0 in (range(move[0][1], move[1][1]) or range(move[1][1], move[0][1])) and \
	0 in (range(move[0][2], move[1][2]) or range(move[1][2], move[0][2])): #up or down 
		#print('f6')
		return False
	elif 0 in (range(move[0][0], move[1][0]) or range(move[1][0], move[0][0])) and \
	move[0][1] == move[1][1] and move[1][1] == 0 and \
	0 in (range(move[0][2], move[1][2]) or range(move[1][2], move[0][2])): # up or down diagonal
		#print('f6')
		return False
	elif 0 in (range(move[0][0], move[1][0]) or range(move[1][0], move[0][0])) and \
	0 in (range(move[0][1], move[1][1]) or range(move[1][1], move[0][1])) and \
	move[0][2] == move[1][2] and move[1][2] == 0:
		#print('f6')
		return False

	# There is a piece between the to and from position
	if not ((move[0][0] == move[1][0] and move[0][1] > move[1][1]) \
		or (move[0][0] == move[1][0] and move[0][1] < move[1][1]) \
		or (move[0][1] == move[1][1] and move[0][0] > move[1][0]) \
		or ( move[0][1] == move[1][1] and move[0][0] < move[1][0]) \
		or (move[0][2] == move[1][2] and move[0][0] < move[1][0]) \
		or (move[0][2] == move[1][2]and move[0][0] > move[1][0]) ):
		#print('Same direction')
		return False

	return True

gameover = False
winningScore = 100
WIN  = 1000
current_depth = 0

def iterativeDeepening():
    while haveTime():
        eval = alphaBeta(current_depth, -200000, 200000)
        current_depth += 1


def haveTime():
    return True

def cube_distance(a, b):
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]), abs(a[2] - b[2]))

#principal variation search (fail-soft version)
def alphaBeta(depth, alpha, beta):
        #move bestmove, current
        if (gameOver or depth <= 0):
        	return winningScore or eval()
        m = firstMove
        makeMove(m)
        current = -alphabeta(depth - 1, -beta, -alpha)
        unmakeMove(m)
        for m in allMoves():
            makeMove(m)
            score = -alphabeta(depth - 1, -alpha-1, -alpha)
            if (score > alpha and score < beta):
                score = -alphabeta(depth - 1, -beta, -alpha)
            unmakeMove(m)
            if (score >= current):
                current = score
                bestmove = m
                if (score >= alpha): alpha = score
                if (score >= beta): break
        
        return current
    
    
def createAllMoves():
	#  Walk in a direction until you hit someone
	plyList = {}
	moves = {}
	Total = 0
	for piecePos in pieceList_map:
		plyList[piecePos] = 0
		moves[(piecePos, DEPTH)] = []
		clash = False

		#if piecePos == (0, -5, 5):
		for direction in range(len(ALL_DIRECTIONS)):
			new = np.array(piecePos)

			for j in range(-5, 5):

				new += ALL_DIRECTIONS[direction]
				move = [piecePos, tuple(new)]
				if tuple(new) in hexboard_map and hexboard_map[tuple(new)] == -1 \
				or not tuple(new) in hexboard_map:
					#print(' not accessible')
					break

				if (new[0] or new[1] or new[2]) > 5 or (new[0] or new[1] or new[2]) < -5:
					#print('Off grid')
					break

				if not validMove(move):
					break

				makeMove(move)
				moves[(move[0], DEPTH)] += [move[1]]
				unmakeMove(move)

				plyList[piecePos] += 1
				Total += 1

	for p in plyList:
		print(p, plyList[p])
	print('Total moves at depth: ', DEPTH, ': ', Total)
	return moves
#import numpy as np
import random as rnd, math
import pandas as pd

zobristKey = 1 # Zobrist key of board position
depth = 0 # the ply in which you perform the search
flag = 0 # exact, alhpa, beta, determines cut off
evaluation = 0 # States if the side to move is ahead
oldEntry = 1 # Entry in table that has been obtained on lower ply
move = [] # The move that was best on a certain depth
historyHash = []
historyZobrist = 1 # store zobrist of from location
side = 1 # 1 = black moves, 0 = white moves
# Index + 1
pieceList = {('F',1): [6, 'N', 14673753767654285510], ('F', 2):[17, 'M', 16429230233791572847], ('F', 3): [28, 'M', 5460759063079358787], ('E', 1): [5, 'P', 16318954180246517971], \
('E', 2): [16, 'P', 11953987020898008829], ('D', 2): [15, 'M', 13266023888163619881], ('G', 1): [7, 'P', 1156566135542422088], ('G', 2): [18, 'P', 15992721674334807719], ('H', 2): [19, 'M', 12746413846889731457], \
('F', 11): [116, 'n', 13507015793297805086], ('F', 10): [105, 'm', 7123177801226663513], \
('F', 9): [94, 'm', 4759767732614604300], ('E', 10): [104, 'p', 14168245320891560355], ('E', 9): [93, 'p', 12553954530247672373], \
('D', 10): [103, 'm', 6690312555934356839], ('G', 10): [106, 'p', 1402378994127889916], ('G', 9): [95, 'p', 5817038718743648036], 
('H', 10): [107, 'm', 15337642794495010922]}

board = {1: -1, 2: -1, 3: -1, 4: -1, 5: 9547937974349114086, 6: 991213505150526537, 7: 10203940492185185489, 8: -1, 9: -1, 10: -1, 11: -1, 12: -1, 13: -1, 14: 11075761370667082023, 15: 11989401954775205416, 16: 2261487428653572425, 17: 14944548638720617981, 18: 6799752729165931035, 19: 8952607927009507782, 20: 12196476491032764289, 21: -1, 22: -1, 23: 1497723679229001448, 24: 15308642353760843742, 25: 4664971474448840787, 26: 14198321289741883116, 27: 1750136006425427714, 28: 12717543261026594042, 29: 1893867868887836679, 30: 6423071005665915649, 31: 17167822520268934647, 32: 1033494776594851253, 33: 12614810231349758038, 34: 12812357701378153022, 35: 6157652093163705960, 36: 11346890750659902489, 37: 6119074642154812525, 38: 6035285078960495647, 39: 18285913770784173976, 40: 14598276339519438766, 41: 13488043949835541439, 42: 6555255413345703737, 43: 3593535859385617564, 44: 13271273125905254681, 45: 8127741213294683337, 46: 11430781601385271689, 47: 9508616239193905430, 48: 3053880333909433669, 49: 6642592222032544942, 50: 17820941620256416265, 51: 15217551683737667953, 52: 13011195941940098661, 53: 17747644324528214990, 54: 17807556656946595473, 55: 3309486206342643222, 56: 11959963355769459955, 57: 11620436813669652349, 58: 6233783362107545723, 59: 18127665983867789043, 60: 2488674194202034277, 61: 10561804596974550131, 62: 11540627113014027829, 63: 18057537740823179037, 64: 18208436570784193895, 65: 14377704025794836245, 66: 15035295000243831590, 67: 3595584847695512963, 68: 1282421462413134087, 69: 10750882590667065227, 70: 14001838571711505490, 71: 10460507007269696930, 72: 4909198791140644574, 73: 4626005788343921385, 74: 10226878675536017708, 75: 1287410972230143095, 76: 14073421603832371045, 77: 14685808712592776252, 78: 17330106233848931619, 79: 3318933992577465589, 80: 2953274606257949061, 81: 5943497566932681161, 82: 5976468406941437725, 83: 4035097654001140978, 84: 16981819976281240079, 85: 18428843069456369071, 86: 4710442358967623234, 87: 15135802444542077879, 88: 14845137964809650869, 89: -1, 90: 12003907947608808087, 91: 8663006492259260488, 92: 11681184246980168227, 93: 6846247378034281785, 94: 10678015506979194509, 95: 11254305699758063, 96: 14407154827763356101, 97: 17667765843890672275, 98: 14721042491670706160, 99: -1, 100: -1, 101: -1, 102: -1, 103: 2467995294121188610, 104: 3854623131305135368, 105: 11909760977978824779, 106: 11846949674743113271, 107: 1830922217091626208, 108: -1, 109: -1, 110: -1, 111: -1, 112: -1, 113: -1, 114: -1, 115: -1, 116: 18005809339750231502, 117: -1, 118: -1, 119: -1, 120: -1, 121:-1}

'''====
>>> my_list1 = [30,34,56]
>>> my_list2 = [29,500,43]

>>> import numpy as np
>>> A_1 = np.array(my_list1)
>>> A_2 = np.array(my_list2)

>>> A_1 >= 30
array([ True,  True,  True], dtype=bool)
>>> A_2 >= 30
array([False,  True,  True], dtype=bool)

>>> ((A_1 >= 30).sum() == A_1.size).astype(np.int)
1
>>> ((A_2 >= 30).sum() == A_2.size).astype(np.int)
0
'''

#class algorithm():
def miniMax(board, depth):
    nodes = 0

    if depth == 0: return 1

    moves = allMoves(board)

    for move in moves:
        makeMove(move, board)
        nodes += miniMax(board, depth-1)
        undoMove(move, board, historyZobrist)

    return nodes


def iterativeDeepening():
    while haveTime():
        eval = alphaBeta(board, current_depth, -200000, 200000, pv)
        current_depth += 1


def haveTime():
    return True


def alphaBeta(board, current_depth, alpha, beta, pv):

    if ply == 0:
        return positionEvaluation

        legalMovesVector = generateMoves()

        for move in legalMovesVector:
            makeMove(move)
            eval = -alphaBeta(ply-1, -beta, -alpha)
            undoMove(move)

            if eval >= beta:
                return beta

            if eval > alpha:
                alpha = eval

    return alpha

def negaMax():
    return 0

def monteCarlo():
    return 0

class HashInput:
  def __init__(self, zobristKey, depth, flag, evaluation, oldEntry, move):
    self.zobrist = zobristKey
    self.depth = depth
    self.flag = flag
    self.eval = evaluation
    self.oldEntry = oldEntry
    self.move = move

h = HashInput(8547732456528787082, 3, 1, 23, 2, [['A', 6], ['A', 8]])

# pieces = np.empty((3, 2, 120))

# Zobrist Key, depth, ply, evaluation, flag (exact, alhpa, beta), best move, old
# Replacement schemes ( always, by depth, always+depth )

'evaluation: In Mediocre the Evaluation method returns a positive score \
 if the side on the move is ahead and a negative score if it is behind.\
 This means +100 means black is ahead if it is black to move when the \
 evaluation is made.'
### [zobrist key]%[total size of the hashtable]
### int hashkey = (int)(zobrist%HASHSIZE)
### 6543248948113846523 % 1000 = 523
### So we store that position at index 523.

#== if(hashentry.depth >= ply)
#==  // Use the values attached

def allMoves(board):
    moves = []
    plyList = {}
    #(('F', 1), [6, 'N', 14673753767654285510]) = piecePos
    for piecePos in pieceList.items():
        plyList[piecePos[0]] = 0
        for position in board:
            r,c = getRowCol(position) # index starts at 1
            move = [[piecePos[0][0], piecePos[0][1]], [c, r]]
            #print('hi', move, piecePos[0], piecePos[0] == ('F', 3))
            if not piecePos[0] == ('F', 3): break
            #print( 'Move', pieceList[piecePos][1], 'from', piecePos[0], 'to', c+str(r))
            if r != 99 and board[position] != -1:
                m = makeMove(move, zobristKey)
                print (m[2], move)

                if  m[2]:
                    #print(drawBoard())
                    moves += [move]
                    undoMove(move, m[0], m[1])
                    plyList[piecePos[0]] += 1

    print ('possible moves', plyList)
    return moves


# Valid move, CONVERT hex NUMBER TO char grid value [A, 9] , [A, 8]
# is the starting position valid and is the to-position still on the board?
def validMove(move):
    A = 65 #ascii value
    # check direction!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    direction = 0 # 0 = vert down, 1 = vert up, 3 = diag, 4 = diag

    #Still on the 11 x 11 grid
    fromMoveValue = move[0][1] * 11 - (11 - (ord(move[0][0]) - A)) +1
    toMoveValue = move[1][1] * 11 - (11 - (ord(move[1][0]) - A)) +1
    
    arrayDistance = abs(toMoveValue - fromMoveValue)
    #check for non move
    if arrayDistance == 0: return False

    # move on board
    if toMoveValue < 1 or toMoveValue > 121 or board[toMoveValue] == -1:
        return False

    if fromMoveValue < 1 or fromMoveValue > 121 or board[fromMoveValue] == -1:
        return False

    #Create list of indexes
    distListKeys = []
    distListValues = []
    for key, value in pieceList.items():
        distListKeys.append(key)
        distListValues.append(value[0])

    r, c = getRowCol(toMoveValue) # get values of to location

    if (c, r) in distListKeys: # Check if there is a piece at this location
        return False

    columns = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K']
    #Distance to adjacent hexagon f#
    base = [2, 2, 1, 1, 0, 0, 0, 1, 1, 2, 2]
    base2 = [-3, -2, -2, -1, -1, 0, 0, 1, 1, 2, 2]

    rowt, colt = getRowCol(toMoveValue)
    rowf, colf = getRowCol(fromMoveValue)
    #basePlus = (pd.Series(base) - base[ord(colt)-A]).tolist()
    basePlus = (pd.Series(base) - base[ord(colf)-A]).tolist()
    basePlus2 = (pd.Series(base2) - base2[ord(colt)-A]).tolist()

    indexf = ord(colf)-A+1
    indext = ord(colt)-A+1

    if rowt > rowf and rowt-rowf > 5: return False
    if rowt < rowf and rowf-rowt > 5: return False

    if colt == colf:

        if rowf > rowt:
            direction = 1 #Up
            #Check if move is possible in vertical up direction
            for r in range(1, rowf-rowt):
                newR = fromMoveValue
                newR -= 11 * r
                newR, c = getRowCol(newR)
                #print(move, r, c, rowf, newR, (c, newR) in distListKeys, 'EE')
                if (c, newR) in distListKeys:
                    return False
                elif r == rowf-rowt-1:
                    return True
        elif rowf < rowt:
            direction = 0 # Down
            #Check if move is possible in vertical down direction
            for r in range(1, (rowt - rowf)+1):
                newR = fromMoveValue
                newR += 11 * r
                newR, c = getRowCol(newR)
                #print(move, r, c, rowt-rowf,'ii', newR, (c, newR) in distListKeys, 'EE')
                if (c, newR) in distListKeys:
                    return False
                elif r == (rowt-rowf):
                    return True

    elif colt < colf:  #base2 = [-3, -2, -2, -1, -1, 0, 0, 1, 1, 2, 2, 3]
       #print( (indexf % 2 == 0 and rowt >= rowf) , (indexf % 2 != 0 and rowt > rowf), rowt+basePlus[indexf] != rowf)
        if indexf % 2 == 0 and rowt >= rowf or indexf % 2 != 0 and rowt > rowf: #drUplD
            direction = 2
            #Check if move is possible in right up to left down diagonal
            for r, c in zip(basePlus[indext:indexf+1], columns[indext:indexf+1]) :
                newR = rowt + r
                #print(move, basePlus[indext:indexf], columns[indext:indexf], r, c, rowf, newR, (c, newR) in distListKeys, rowt+basePlus[indexf] != rowf, 'BB')
                if (c, newR) in distListKeys or rowt+basePlus[indext-1] == rowf:
                    return False
                elif r == indexf+1:
                    return True

        elif indexf % 2 == 0 and rowt < rowf or indexf % 2 != 0 and rowt < rowf: #drDlUp
            direction = 3
            #Check if move is possible in RightDown to LeftUp diagonal
            for r, c in zip(basePlus2[indext:indexf-1], columns[indext:indexf]) :
                newR = rowt + r
                #print(move, basePlus2[indext:indexf-1], columns[indext:indexf-1], r, c, rowf, newR, (c, newR) in distListKeys, rowt+basePlus[indexf] != rowf, 'BB')
                if (c, newR) in distListKeys or rowf+basePlus2[indexf-1] == rowt:
                    return False
                elif r == indexf-1:
                    return True
    elif colt > colf:
        if (indexf % 2 == 0 and rowt >= rowf) or (indexf % 2 != 0 and rowt > rowf): #dlUprD
            #Check if move is possible in leftUp to rightDown diagonal
            for r, c in zip(basePlus[indexf:indext+1], columns[indexf:indext+1]) :
                newR = rowf + r
               #print(rowf+basePlus[indext-1] == rowt, indexf, rowf+basePlus[indext-1], rowt)
               #print(move, basePlus[indexf:indext-1], columns[indexf:indext-1], r, c, rowf, newR, (c, newR) in distListKeys, rowt+basePlus2[indexf] != rowf, 'DD')
                if (c, newR) in distListKeys or rowf + basePlus[indext-1] != rowt:
                    return False
                elif rowf + basePlus[indext-1] == rowt:
                    return True

        elif (indexf % 2 == 0 and rowt < rowf) or (indexf % 2 != 0 and rowt < rowf): #dlDrUp
            direction = 5
            #Check if move is possible in leftDown to rightUp diagonal
            for r, c in zip(basePlus2[indexf-1:indext-1], columns[indexf:indext-1]) :
                newR = rowf + r
               # print(rowf+basePlus2[indext] == rowt, rowf+basePlus2[indext], rowt)
                if (c, newR) in distListKeys or rowf+basePlus2[indext-1] == rowt:
                    return False
                elif r == indext-1:
                    return True
    else:
        return True


def makeMove(move, board):

    zobristKey = board
    if validMove(move):
        zobristKey ^= board
    else:
        return [zobristKey, pieceList[(move[0][0], move[0][1])][2], False]

    pieceList[(move[1][0], move[1][1])] = ['x', 'x', rnd.getrandbits(64)]
    pieceList[(move[1][0], move[1][1])][0] = pieceList[(move[0][0], move[0][1])][0]
    pieceList[(move[1][0], move[1][1])][1] = pieceList[(move[0][0], move[0][1])][1]
    historyZobrist = pieceList[(move[0][0], move[0][1])][2]
    # Update Zobrist key board
    zobristKey ^= pieceList[(move[0][0], move[0][1])][2]
    zobristKey ^= pieceList[(move[1][0], move[1][1])][2]
    del pieceList[(move[0][0], move[0][1])]

    return [zobristKey, historyZobrist, True]

def undoMove(move, board, historyZobrist):

    zobristKey = board
    print('undo:', move)
    pieceList[(move[0][0], move[0][1])] = ['x', 'x', historyZobrist]
    pieceList[(move[0][0], move[0][1])][0] = pieceList[(move[1][0], move[1][1])][0]
    pieceList[(move[0][0], move[0][1])][1] = pieceList[(move[1][0], move[1][1])][1]

    # Update Zobrist key board
    zobristKey ^= pieceList[(move[0][0], move[0][1])][2]
    zobristKey ^= pieceList[(move[1][0], move[1][1])][2]
    del pieceList[(move[1][0], move[1][1])]

    return zobristKey

# initialize board
def boardInit(board):
    zobristKey = 0
    distList = []
    for key, value in pieceList:
        distList.append(key)

    for pos in board:
        r, c = getRowCol(pos)
        if board[pos] != -1:
            zobristKey ^= board[pos]
            try:
                distList.index((c,r)) # Check if there is a piece at this location
                zobristKey ^= pieceList[(c, r)][2]
            except ValueError:
                ''
    return zobristKey


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

def drawBoard():
    col = 'A'
    row = 1
    strs = '' # boardString, hex format

    for pos in board:

        row, col = getRowCol(pos) #convert to [A, 1] format

        if (col, row) in pieceList:
            if board[pos] != -1:
                strs += ' ' + str(pieceList[(col, row)][1])
            elif board[pos] == -1:
                strs += ' '  #str(board[pos])
        else:
            if board[pos] != -1:
                strs += ' ' + '-'
            elif board[pos] == -1:
                strs += '  ' #str(board[pos])

        # Next line, use for creating a board
        if pos > 0 and pos % 11 == 0:
            strs += '\n'
            if pos % 2 == 0:
                strs += ''

    return '\n' + strs
'''
print drawBoard(),\
'\nInitial zobrist board: ', makeMove([['F', 3] , ['F', 5]], boardInit(board))
print drawBoard(), \
'\nNew zobrist board: ', boardInit(board), boardInit(board) % 100'''
zobristKey =  boardInit(board)
#print 'miniMax', miniMax(board, 5)
allMoves(board)
for x in range(-5, 6):
    for y in range(-5, 6):
        print ((y, x), ': ', rnd.getrandbits(64), ',')
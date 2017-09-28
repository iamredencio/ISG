#import numpy as np
import random as rnd, math

zobristKey = 1L; # Zobrist key of board position
depth = 0; # the ply in which you perform the search
flag = 0; # exact, alhpa, beta, determines cut off
evaluation = 0; # States if the side to move is ahead
oldEntry = 1; # Entry in table that has been obtained on lower ply
move = []; # The move that was best on a certain depth

class HashInput:
  def __init__(self, zobristKey, depth, flag, evaluation, oldEntry, move):
    self.zobrist = zobristKey;
    self.depth = depth;
    self.flag = flag;
    self.eval = evaluation;
    self.oldEntry = oldEntry;
    self.move = move;

h = HashInput(8547732456528787082, 3, 1, 23, 2, [['A', 6], ['A', 8]])

# pieces = np.empty((3, 2, 120))

# Zobrist Key, depth, ply, evaluation, flag (exact, alhpa, beta), best move, old
# Replacement schemes ( always, by depth, always+depth )

'evaluation: In Mediocre the Evaluation method returns a positive score \
 if the side on the move is ahead and a negative score if it is behind.\
 This means +100 means black is ahead if it is black to move when the \
 evaluation is made.'
### [zobrist key]%[total size of the hashtable]
### int hashkey = (int)(zobrist%HASHSIZE);
### 6543248948113846523 % 1000 = 523
### So we store that position at index 523.

#== if(hashentry.depth >= ply)
#==  // Use the values attached

# Index + 1
pieceList = {('F',1): [6, 'N', 14673753767654285510], ('F', 2):[17, 'M', 16429230233791572847], ('F', 3): [28, 'M', 5460759063079358787], ('E', 1): [5, 'P', 16318954180246517971], \
('E', 2): [16, 'P', 11953987020898008829], ('D', 2): [15, 'M', 13266023888163619881], ('G', 1): [7, 'P', 1156566135542422088], ('G', 2): [18, 'P', 15992721674334807719], ('H', 2): [19, 'M', 12746413846889731457], \
('F', 11): [116, 'n', 13507015793297805086], ('F', 10): [105, 'm', 7123177801226663513], ('F', 9): [94, 'm', 4759767732614604300], ('E', 10): [104, 'p', 14168245320891560355], ('E', 9): [93, 'p', 12553954530247672373], \
('D', 10): [103, 'm', 6690312555934356839], ('G', 10): [106, 'p', 1402378994127889916], ('G', 9): [95, 'p', 5817038718743648036], ('H', 10): [107, 'm', 15337642794495010922]}

board = {1: -1, 2: -1, 3: -1, 4: -1, 5: 9547937974349114086L, 6: 991213505150526537L, 7: 10203940492185185489L, 8: -1, 9: -1, 10: -1, 11: -1, 12: -1, 13: -1, 14: 11075761370667082023L, 15: 11989401954775205416L, 16: 2261487428653572425L, 17: 14944548638720617981L, 18: 6799752729165931035L, 19: 8952607927009507782L, 20: 12196476491032764289L, 21: -1, 22: -1, 23: 1497723679229001448L, 24: 15308642353760843742L, 25: 4664971474448840787L, 26: 14198321289741883116L, 27: 1750136006425427714L, 28: 12717543261026594042L, 29: 1893867868887836679L, 30: 6423071005665915649L, 31: 17167822520268934647L, 32: 1033494776594851253L, 33: 12614810231349758038L, 34: 12812357701378153022L, 35: 6157652093163705960L, 36: 11346890750659902489L, 37: 6119074642154812525L, 38: 6035285078960495647L, 39: 18285913770784173976L, 40: 14598276339519438766L, 41: 13488043949835541439L, 42: 6555255413345703737L, 43: 3593535859385617564L, 44: 13271273125905254681L, 45: 8127741213294683337L, 46: 11430781601385271689L, 47: 9508616239193905430L, 48: 3053880333909433669L, 49: 6642592222032544942L, 50: 17820941620256416265L, 51: 15217551683737667953L, 52: 13011195941940098661L, 53: 17747644324528214990L, 54: 17807556656946595473L, 55: 3309486206342643222L, 56: 11959963355769459955L, 57: 11620436813669652349L, 58: 6233783362107545723L, 59: 18127665983867789043L, 60: 2488674194202034277L, 61: 10561804596974550131L, 62: 11540627113014027829L, 63: 18057537740823179037L, 64: 18208436570784193895L, 65: 14377704025794836245L, 66: 15035295000243831590L, 67: 3595584847695512963L, 68: 1282421462413134087L, 69: 10750882590667065227L, 70: 14001838571711505490L, 71: 10460507007269696930L, 72: 4909198791140644574L, 73: 4626005788343921385L, 74: 10226878675536017708L, 75: 1287410972230143095L, 76: 14073421603832371045L, 77: 14685808712592776252L, 78: 17330106233848931619L, 79: 3318933992577465589L, 80: 2953274606257949061L, 81: 5943497566932681161L, 82: 5976468406941437725L, 83: 4035097654001140978L, 84: 16981819976281240079L, 85: 18428843069456369071L, 86: 4710442358967623234L, 87: 15135802444542077879L, 88: 14845137964809650869L, 89: -1, 90: 12003907947608808087L, 91: 8663006492259260488L, 92: 11681184246980168227L, 93: 6846247378034281785L, 94: 10678015506979194509L, 95: 11254305699758063L, 96: 14407154827763356101L, 97: 17667765843890672275L, 98: 14721042491670706160L, 99: -1, 100: -1, 101: -1, 102: -1, 103: 2467995294121188610L, 104: 3854623131305135368L, 105: 11909760977978824779L, 106: 11846949674743113271L, 107: 1830922217091626208L, 108: -1, 109: -1, 110: -1, 111: -1, 112: -1, 113: -1, 114: -1, 115: -1, 116: 18005809339750231502L, 117: -1, 118: -1, 119: -1, 120: -1, 121:-1}

# Valid move, CONVERT hex NUMBER TO char grid value [A, 9] , [A, 8]
# is the starting position valid and is the to-position still on the board?
def validMove(move):
    A = 65 #ascii value

    #Still on the 11 x 11 grid
    fromMoveValue = move[0][1] * 11 - (11 - (ord(move[0][0]) - A)) +1
    toMoveValue = move[1][1] * 11 - (11 - (ord(move[1][0]) - A)) +1

    if toMoveValue < 0 or toMoveValue > 121 or board[toMoveValue] == -1:
        return False

    if fromMoveValue < 0 or fromMoveValue > 121 or board[fromMoveValue] == -1:
        return False

    #Create list of indexes
    distListKeys = []
    distListValues = []
    for key, value in pieceList.iteritems():
        distListKeys.append(key)
        distListValues.append(value[0])

    r, c = getRowCol(toMoveValue-1) # get values of to location

    try:
        if (c, r) in distListKeys: # Check if there is a piece at this location
          print 'Occupied', r, c
          return False
    except ValueError:
        print 'Vacant', r, c
        return False

    # Check if the move is valid vertically or diagonally
    vert = [11, 22, 33, 44, 55, 66, 77, 88, 99, 110, 121]
    leftUpRightDiag = [12, 13, 25, 26, 38, 39, 51, 52, 64, 65] #0 - 121
    rightUpLeftDiag = [10, 9, 19, 18, 28, 27, 37, 36, 46, 45] #121 - 0

    d = [] # direction

    # Distance between from and to location
    distance = abs(fromMoveValue - toMoveValue)

    if distance in vert:
      print 'Vertical move', abs(fromMoveValue - toMoveValue), toMoveValue
      d = vert
     # return True
    elif distance-1 in leftUpRightDiag:
      print 'Diagonal LeftUpRight move', abs(fromMoveValue - toMoveValue)-1
      d = leftUpRightDiag
     # return True
    elif distance in rightUpLeftDiag:
      print 'Diagonal rightUpLeft move', abs(fromMoveValue - toMoveValue)
      d = rightUpLeftDiag
      #return True
    else:
      return False

    # Check if there is another piece in the between the from and to location
    diagonalCheckDown = [distance - v for v in d]
    diagonalCheckUp = [distance + v for v in d]
    vertCheckUp = [fromMoveValue + v for v in d]
    vertCheckDown = [fromMoveValue - v for v in d]

    down = list(set(diagonalCheckDown) & set(distListValues))
    if down  != []:
      print 'Down diagonal occupied locations: ', down
      return False

    up = list(set(diagonalCheckUp) & set(distListValues))
    if up  != []:
      print 'Up diagional occupied locations: ', up
      return False

    down = list(set(vertCheckDown) & set(distListValues))
    if down  != []:
      print 'Down vertical occupied locations: ', down
      return False

    up = list(set(vertCheckUp) & set(distListValues))
    if up  != []:
      print 'Up vertical occupied locations: ', up
      return False

    f6_location = [61]
    if list(set(diagonalCheckUp) & set(f6_location)) != [] \
    or list(set(diagonalCheckDown) & set(f6_location)) != [] \
    or list(set(vertCheckUp) & set(f6_location)) != [] \
    or list(set(vertCheckDown) & set(f6_location)) != []:
        print 'You can not cross F6'
        return False
    # Default assumption is that everything fits within a 11 x 11 grid
    return True

def makeMove(move, board):

    zobristKey = board
    if validMove(move):
        zobristKey ^= board
    else:
        return zobristKey

    pieceList[(move[1][0], move[1][1])] = ['x', 'x', rnd.getrandbits(64)]
    pieceList[(move[1][0], move[1][1])][0] = pieceList[(move[0][0], move[0][1])][0]
    pieceList[(move[1][0], move[1][1])][1] = pieceList[(move[0][0], move[0][1])][1]

    # Update Zobrist key board
    zobristKey ^= pieceList[(move[0][0], move[0][1])][2]
    zobristKey ^= pieceList[(move[1][0], move[1][1])][2]
    del pieceList[(move[0][0], move[0][1])]

    return zobristKey

# initialize board
def boardInit(board):
    zobristKey = 0
    distList = []
    for key, value in pieceList.iteritems():
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
        # Row decides the value of the number for ex. f11: row = 11
        row = [0, 11, 22, 33, 44, 55, 66, 77, 88, 99, 110].index(pos)
        col = 'A' #ascii 65
        return [row, col]
    except ValueError:
        pass

    try:
        row = [1, 12, 23, 34, 45, 56, 67, 78, 89, 100, 111].index(pos)+1
        col = 'B' #66
        return [row, col]
    except ValueError:
        pass

    try:
        row = [2, 13, 24, 35, 46, 57, 68, 79, 90, 101, 112].index(pos)+1
        col = 'C' #67
        return [row, col]
    except ValueError:
        pass

    try:
        row = [3, 14, 25, 36, 47, 58, 69, 80, 91, 102, 113].index(pos)+1
        col = 'D' #68
        return [row, col]
    except ValueError:
        pass

    try:
        row = [4, 15, 26, 37, 48, 59, 70, 81, 92, 103, 114].index(pos)+1
        col = 'E' #69
        return [row, col]
    except ValueError:
        pass

    try:
        row = [5, 16, 27, 38, 49, 60, 71, 82, 93, 104, 115].index(pos)+1
        col = 'F' #70
        return [row, col]
    except ValueError:
        pass

    try:
        row = [6, 17, 28, 39, 50, 61, 72, 83, 94, 105, 116].index(pos)+1
        col = 'G' #71
        return [row, col]
    except ValueError:
        pass

    try:
        row = [7, 18, 29, 40, 51, 62, 73, 84, 95, 106, 117].index(pos)+1
        col = 'H' #72
        return [row, col]
    except ValueError:
        pass

    try:
        row = [8, 19, 30, 41, 52, 63, 74, 85, 96, 107, 118].index(pos)+1
        col = 'I' #73
        return [row, col]
    except ValueError:
        pass

    try:
        row = [9, 20, 31, 42, 53, 64, 75, 86, 97, 108, 119].index(pos)+1
        col = 'J' #74
        return [row, col]
    except ValueError:
        pass

    try:
        row = [10, 21, 32, 43, 54, 65, 76, 87, 98, 109, 120].index(pos)+1
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

        row, col = getRowCol(pos-1) #convert to [A, 1] format

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

print drawBoard(),\
'\nInitial zobrist board: ', makeMove([['F', 1] , ['F', 7]], boardInit(board))
print drawBoard(), \
'\nNew zobrist board: ', boardInit(board), boardInit(board) % 100

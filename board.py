import numpy as np



pieces = np.empty((3, 2, 120))
board = {1: -1, 2: -1, 3: -1, 4: -1, 5: 9547937974349114086L, 6: 991213505150526537L, 7: 10203940492185185489L, 8: -1, 9: -1, 10: -1, 11: -1, 12: -1, 13: -1, 14: 11075761370667082023L, 15: 11989401954775205416L, 16: 2261487428653572425L, 17: 14944548638720617981L, 18: 6799752729165931035L, 19: 8952607927009507782L, 20: 12196476491032764289L, 21: -1, 22: -1, 23: 1497723679229001448L, 24: 15308642353760843742L, 25: 4664971474448840787L, 26: 14198321289741883116L, 27: 1750136006425427714L, 28: 12717543261026594042L, 29: 1893867868887836679L, 30: 6423071005665915649L, 31: 17167822520268934647L, 32: 1033494776594851253L, 33: 12614810231349758038L, 34: 12812357701378153022L, 35: 6157652093163705960L, 36: 11346890750659902489L, 37: 6119074642154812525L, 38: 6035285078960495647L, 39: 18285913770784173976L, 40: 14598276339519438766L, 41: 13488043949835541439L, 42: 6555255413345703737L, 43: 3593535859385617564L, 44: 13271273125905254681L, 45: 8127741213294683337L, 46: 11430781601385271689L, 47: 9508616239193905430L, 48: 3053880333909433669L, 49: 6642592222032544942L, 50: 17820941620256416265L, 51: 15217551683737667953L, 52: 13011195941940098661L, 53: 17747644324528214990L, 54: 17807556656946595473L, 55: 3309486206342643222L, 56: 11959963355769459955L, 57: 11620436813669652349L, 58: 6233783362107545723L, 59: 18127665983867789043L, 60: 2488674194202034277L, 61: 10561804596974550131L, 62: 11540627113014027829L, 63: 18057537740823179037L, 64: 18208436570784193895L, 65: 14377704025794836245L, 66: 15035295000243831590L, 67: 3595584847695512963L, 68: 1282421462413134087L, 69: 10750882590667065227L, 70: 14001838571711505490L, 71: 10460507007269696930L, 72: 4909198791140644574L, 73: 4626005788343921385L, 74: 10226878675536017708L, 75: 1287410972230143095L, 76: 14073421603832371045L, 77: 14685808712592776252L, 78: 17330106233848931619L, 79: 3318933992577465589L, 80: 2953274606257949061L, 81: 5943497566932681161L, 82: 5976468406941437725L, 83: 4035097654001140978L, 84: 16981819976281240079L, 85: 18428843069456369071L, 86: 4710442358967623234L, 87: 15135802444542077879L, 88: 14845137964809650869L, 89: -1, 90: 12003907947608808087L, 91: 8663006492259260488L, 92: 11681184246980168227L, 93: 6846247378034281785L, 94: 10678015506979194509L, 95: 11254305699758063L, 96: 14407154827763356101L, 97: 17667765843890672275L, 98: 14721042491670706160L, 99: -1, 100: -1, 101: -1, 102: -1, 103: 2467995294121188610L, 104: 3854623131305135368L, 105: 11909760977978824779L, 106: 11846949674743113271L, 107: 1830922217091626208L, 108: -1, 109: -1, 110: -1, 111: -1, 112: -1, 113: -1, 114: -1, 115: -1, 116: 18005809339750231502L, 117: -1, 118: -1, 119: -1, 120: -1, 121:-1}

#Valid move, CONVERT NUMBER TO char value [A, 9] , [A, 8]
# is the starting position valid and is the to poisition on the board still?
def validMove(move):
    difHorz = ord(move[0][0]) - ord(move[1][0]) #horz distance - left,  + right
    difVert = move[0][1] - move[1][1] #vertical distance - up,  + down

    # Check if on the board after a move and moving in the vertical direction
    # else check if move still on board
    if difHorz == 0:
        if difVert > 0 and move[0][1] + 27 <= 120: return True
        elif difVert < 0 and move[0][1] - 27 >= 0: return True
    elif move[1][0] in ['A', 'B', 'K', 'J'] and move[1][1] < 3 : return False
    elif move[1][0] in ['C', 'D', 'H', 'I'] and move[1][1] < 2: return False
    elif move[1][0] in ['B', 'C', 'I', 'J'] and move[1][1] > 9 : return False
    elif move[1][0] in ['A', 'K'] and move[1][1] > 8: return False
    elif move[1][0] in ['D', 'E', 'G', 'H'] and move[1][1] > 8: return False

    # Default is that everything fits within a 11 x 11 grid
    return (ord(move[0][0]) > 63 and ord(move[0][0]) < 76) and \
    (ord(move[1][0]) > 63 and ord(move[1][0]) < 76) and  \
    (move[0][1] > 0 and move[0][1] < 12) and (move[1][1] > 0 and move[1][1] < 12)


def makeMove(move):
    zobristKey = 0
    if validMove(move):
        zobristKey ^= 1

    #zobristKey ^= Zobrist.PIECES[2][0][move[0][1]];
    #zobristKey ^= Zobrist.PIECES[2][0][move[1][1]];

    return 0

# initialize board
def boardInit(board):
    zobristKey = 0
    for pos in board:
        if board[pos] != -1:
            zobristKey ^= board[pos]
    return zobristKey
'''
  int piece = board.boardArray[index];
  if(piece > 0) // White piece
    zobristKey ^= PIECES[Math.abs(piece)-1][0][index];
  else if(piece < 0) // Black piece
      zobristKey ^= PIECES[Math.abs(piece)-1][1][index];
'''

strs = ''
oddEven = 0

for pos in board:

    if pos == 1:
        strs += ' '

    #pos += 1 # set start index to 1, use for modulo 11

    if board[pos] != -1:
        strs += ' ' + 'X' #str(board[pos])
    elif board[pos] == -1:
        strs += ' ' + '_' #str(board[pos])

    if pos > 0 and pos % 11 == 0:
        strs += '\n'
        if pos % 2 == 0:
            strs += ' '
        oddEven = 1

print makeMove([['A', 8] , ['A', 13]]), boardInit(board)
print strs, len(board)

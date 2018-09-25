import numpy as np
CHECKER_VALUE = 1000
MAX_LEVEL = 1

#val
def val(matrix, player, net_value = False):
    p1p = 0
    p2p = 0
    for row in matrix:
        for box in row:
            if box == 1:
                p1p = p1p + 1
            elif box == 3:
                p1p = p1p + CHECKER_VALUE
            if box == 2:
                p2p = p2p + 1
            elif box == 4:
                p2p = p2p + CHECKER_VALUE

    if net_value and player == 1:
        return p1p
    elif net_value and player == 2:
        return p2p

    if player == 1:
        return p1p - p2p
    elif player == 2:
        return p2p - p1p
    else:
        raise

#remove_checkers
def remove_checkers(matrix, player, i, j):

    row = i
    col = j
    moves1 = []
    moves2 = []
    moves3 = []
    moves4 = []

    if player == 1:
        if row - 2 >= 0 and col - 2 >= 0 and (matrix[row-1,col-1] == 2 or matrix[row-1,col-1] == 4) and matrix[row-2,col-2] == 0:
            new_matrix = np.copy(matrix)
            new_matrix[row-1,col-1] = 0
            moves1 = remove_checkers(new_matrix, player, row-2, col-2)
            for move in moves1:
                move.append((row-1,col-1))

        if row - 2 >= 0 and col + 2 < 8 and (matrix[row-1,col+1] == 2 or matrix[row-1,col+1] == 4) and matrix[row-2,col+2] == 0:
            new_matrix = np.copy(matrix)
            new_matrix[row-1,col+1] = 0
            moves2 = remove_checkers(new_matrix, player, row-2, col+2)
            for move in moves2:
                move.append((row-1,col+1))

        return moves1 + moves2 + [[(row,col)]]

    elif player == 2:
        if row + 2 < 8  and col - 2 >= 0 and (matrix[row+1,col-1] == 1 or matrix[row+1,col-1] == 3) and matrix[row+2,col-2] == 0:
            new_matrix = np.copy(matrix)
            new_matrix[row+1,col-1] = 0
            moves1 = remove_checkers(new_matrix, player, row+2, col-2)
            for move in moves1:
                move.append((row+1,col-1))

        if row + 2 < 8 and col + 2 < 8 and (matrix[row+1,col+1] == 1 or matrix[row+1,col+1] == 3) and matrix[row+2,col+2] == 0:
            new_matrix = np.copy(matrix)
            new_matrix[row+1,col+1] = 0
            moves2 = remove_checkers(new_matrix, player, row+2, col+2)
            for move in moves2:
                move.append((row+1,col+1))

        return moves1 + moves2 + [[(row,col)]]

    elif player == 3:
        if row - 2 >= 0 and col - 2 >= 0 and (matrix[row-1,col-1] == 2 or matrix[row-1,col-1] == 4) and matrix[row-2,col-2] == 0:
            new_matrix = np.copy(matrix)
            new_matrix[row-1,col-1] = 0
            moves1 = remove_checkers(new_matrix, player, row-2, col-2)
            for move in moves1:
                move.append((row-1,col-1))

        if row - 2 >= 0 and col + 2 < 8 and (matrix[row-1,col+1] == 2 or matrix[row-1,col+1] == 4) and matrix[row-2,col+2] == 0:
            new_matrix = np.copy(matrix)
            new_matrix[row-1,col+1] = 0
            moves2 = remove_checkers(new_matrix, player, row-2, col+2)
            for move in moves2:
                move.append((row-1,col+1))

        if row + 2 < 8  and col - 2 >= 0 and (matrix[row+1,col-1] == 2 or matrix[row+1,col-1] == 4) and matrix[row+2,col-2] == 0:
            new_matrix = np.copy(matrix)
            new_matrix[row+1,col-1] = 0
            moves3 = remove_checkers(new_matrix, player, row+2, col-2)
            for move in moves3:
                move.append((row+1,col-1))

        if row + 2 < 8 and col + 2 < 8 and (matrix[row+1,col+1] == 2 or matrix[row+1,col+1] == 4) and matrix[row+2,col+2] == 0:
            new_matrix = np.copy(matrix)
            new_matrix[row+1,col+1] = 0
            moves4 = remove_checkers(new_matrix, player, row+2, col+2)
            for move in moves4:
                move.append((row+1,col+1))

        return moves1 + moves2 + moves3 + moves4 + [[(row,col)]]

    elif player == 4:
        if row - 2 >= 0 and col - 2 >= 0 and (matrix[row-1,col-1] == 1 or matrix[row-1,col-1] == 3) and matrix[row-2,col-2] == 0:
            new_matrix = np.copy(matrix)
            new_matrix[row-1,col-1] = 0
            moves1 = remove_checkers(new_matrix, player, row-2, col-2)
            for move in moves1:
                move.append((row-1,col-1))

        if row - 2 >= 0 and col + 2 < 8 and (matrix[row-1,col+1] == 1 or matrix[row-1,col+1] == 3) and matrix[row-2,col+2] == 0:
            new_matrix = np.copy(matrix)
            new_matrix[row-1,col+1] = 0
            moves2 = remove_checkers(new_matrix, player, row-2, col+2)
            for move in moves2:
                move.append((row-1,col+1))

        if row + 2 < 8  and col - 2 >= 0 and (matrix[row+1,col-1] == 1 or matrix[row+1,col-1] == 3) and matrix[row+2,col-2] == 0:
            new_matrix = np.copy(matrix)
            new_matrix[row+1,col-1] = 0
            moves3 = remove_checkers(new_matrix, player, row+2, col-2)
            for move in moves3:
                move.append((row+1,col-1))

        if row + 2 < 8 and col + 2 < 8 and (matrix[row+1,col+1] == 1 or matrix[row+1,col+1] == 3) and matrix[row+2,col+2] == 0:
            new_matrix = np.copy(matrix)
            new_matrix[row+1,col+1] = 0
            moves4 = remove_checkers(new_matrix, player, row+2, col+2)
            for move in moves4:
                move.append((row+1,col+1))

        return moves1 + moves2 + moves3 + moves4 +  [[(row,col)]]
    else:
        raise

#give_moves
def give_moves(matrix,player):
    moves = []

    for row_i in range(0,matrix.shape[0]):
        for col_j in range(0,matrix.shape[1]):

            if matrix[row_i,col_j] == 1 and player == 1:
                if row_i - 1 >= 0 and col_j - 1 >= 0 and matrix[row_i-1,col_j-1] == 0:
                    moves.append([(row_i-1,col_j-1),1,(row_i,col_j)])
                if row_i - 1 >= 0 and col_j + 1 < 8 and matrix[row_i-1,col_j+1] == 0:
                    moves.append([(row_i-1,col_j+1),1,(row_i,col_j)])
                temp_moves = remove_checkers(matrix,1,row_i,col_j)
                for move in temp_moves:
                    temptup = move[-1]
                    if temptup[0] != row_i or temptup[1] != col_j:
                        move = move + [1,(row_i,col_j)]
                        moves.append(move)

            if matrix[row_i,col_j] == 2 and player == 2:
                if row_i + 1 < 8 and col_j - 1 >= 0 and matrix[row_i+1,col_j-1] == 0:
                    moves.append([(row_i+1,col_j-1),2,(row_i,col_j)])
                if row_i + 1 < 8 and col_j + 1 < 8 and matrix[row_i+1,col_j+1] == 0:
                    moves.append([(row_i+1,col_j+1),2,(row_i,col_j)])
                temp_moves = remove_checkers(matrix,2,row_i,col_j)
                for move in temp_moves:
                    temptup = move[-1]
                    if temptup[0] != row_i or temptup[1] != col_j:
                        move = move + [2,(row_i,col_j)]
                        moves.append(move)

            if matrix[row_i,col_j] == 3 and player == 1:
                if row_i + 1 < 8 and col_j - 1 >= 0 and matrix[row_i+1,col_j-1] == 0:
                    moves.append([(row_i+1,col_j-1),matrix[row_i,col_j],(row_i,col_j)])
                if row_i + 1 < 8 and col_j + 1 < 8 and matrix[row_i+1,col_j+1] == 0:
                    moves.append([(row_i+1,col_j+1),matrix[row_i,col_j],(row_i,col_j)])
                if row_i - 1 >= 0 and col_j - 1 >= 0 and matrix[row_i-1,col_j-1] == 0:
                    moves.append([(row_i-1,col_j-1),matrix[row_i,col_j],(row_i,col_j)])
                if row_i - 1 >= 8 and col_j + 1 < 8 and matrix[row_i-1,col_j+1] == 0:
                    moves.append([(row_i-1,col_j+1),matrix[row_i,col_j],(row_i,col_j)])
                temp_moves = remove_checkers(matrix,matrix[row_i,col_j],row_i,col_j)
                for move in temp_moves:
                    temptup = move[-1]
                    if temptup[0] != row_i or temptup[1] != col_j:
                        move = move + [matrix[row_i,col_j],(row_i,col_j)]
                        moves.append(move)

            if matrix[row_i,col_j] == 4 and player == 2:
                if row_i + 1 < 8 and col_j - 1 >= 0 and matrix[row_i+1,col_j-1] == 0:
                    moves.append([(row_i+1,col_j-1),matrix[row_i,col_j],(row_i,col_j)])
                if row_i + 1 < 8 and col_j + 1 < 8 and matrix[row_i+1,col_j+1] == 0:
                    moves.append([(row_i+1,col_j+1),matrix[row_i,col_j],(row_i,col_j)])
                if row_i - 1 >= 0 and col_j - 1 >= 0 and matrix[row_i-1,col_j-1] == 0:
                    moves.append([(row_i-1,col_j-1),matrix[row_i,col_j],(row_i,col_j)])
                if row_i - 1 >= 0 and col_j + 1 < 8 and matrix[row_i-1,col_j+1] == 0:
                    moves.append([(row_i-1,col_j+1),matrix[row_i,col_j],(row_i,col_j)])
                temp_moves = remove_checkers(matrix,matrix[row_i,col_j],row_i,col_j)
                for move in temp_moves:
                    temptup = move[-1]
                    if temptup[0] != row_i or temptup[1] != col_j:
                        move = move + [matrix[row_i,col_j],(row_i,col_j)]
                        moves.append(move)

    return moves

#calc_state
def calc_state(matrix,move):
    new_matrix = np.zeros((8,8)).astype(np.int8)
    for row_i in range(0,matrix.shape[0]):
        for col_j in range(0,matrix.shape[1]):
            new_matrix[row_i,col_j] = matrix[row_i,col_j]
    for i in range(len(move)):
        if i > 0 and i < len(move) - 2:
            tuple = move[i]
            new_matrix[tuple[0],tuple[1]] = 0
    newloc = move[0]
    if move[-2] == 1 and newloc[0] == 0:
        new_matrix[newloc[0],newloc[1]] = 3
    elif move[-2] == 2 and newloc[0] == 7:
        new_matrix[newloc[0],newloc[1]] = 4
    else:
        new_matrix[newloc[0],newloc[1]] = move[-2]
    oldloc = move[-1]
    new_matrix[oldloc[0],oldloc[1]] = 0
    return new_matrix

#rec_best_move
def rec_best_move(level, state, player):
    values1 = []
    min_val = None
    max_val = None
    sbreak = False
    opp = 2 if player == 1 else 1
    if level == 0:
        return ([],val(state,player))
    else:
        moves = give_moves(state,player)
        for move in moves:
            values2 = []
            nxtState1 = calc_state(state,move)
            opp_moves = give_moves(nxtState1,opp)
            for opp_move in opp_moves:
                nxtState2 = calc_state(nxtState1,opp_move)
                tup = rec_best_move(level-1,nxtState2,player)
                if tup:
                    values2.append(tup[1])
                else:
                    sbreak = True
                    break
            if sbreak:
                break
            if len(values2) != 0:
                min_val = min(values2)
                values1.append(min_val)
        if not sbreak and len(values1) != 0:
            max_val = max(values1)
            ind = values1.index(max_val)
            return (moves[ind],max_val)
        else:
            return None

#calc_best_move
def calc_best_move(matrix,player):
    tup = rec_best_move(MAX_LEVEL,matrix,player)
    if tup:
        return tup[0]
    else:
        return None

#give_nxtState
def give_nxtState(state,player):
    move = calc_best_move(state,player)
    new_state = calc_state(state,move)
    return new_state

#play
def play():
    matrix = np.zeros((8,8)).astype(np.int8)

    matrix[0,1] = 2
    matrix[0,3] = 2
    matrix[0,5] = 2
    matrix[0,7] = 2
    matrix[1,0] = 2
    matrix[1,2] = 2
    matrix[1,4] = 2
    matrix[1,6] = 2
    matrix[2,1] = 2
    matrix[2,3] = 2
    matrix[2,5] = 2
    matrix[2,7] = 2

    matrix[5,0] = 1
    matrix[5,2] = 1
    matrix[5,4] = 1
    matrix[5,6] = 1
    matrix[6,1] = 1
    matrix[6,3] = 1
    matrix[6,5] = 1
    matrix[6,7] = 1
    matrix[7,0] = 1
    matrix[7,2] = 1
    matrix[7,4] = 1
    matrix[7,6] = 1

    player = 1
    while val(matrix,1,net_value = True) != 0 and val(matrix,2,net_value = True) != 0:
        print(matrix)
        print(player)
        move = calc_best_move(matrix,player)
        print(move)
        if move:
            matrix = calc_state(matrix,move)
        else:
            print("No one wins")
            break
        player = 2 if player == 1 else 1
    print(matrix)
    if val(matrix,1,net_value = True) == 0:
        return 2
    else:
        return 1

# Test
# matrix = np.zeros((8,8))
#
# matrix[3,2] = 1
# matrix[4,1] = 3
# matrix[4,3] = 2
# matrix[4,7] = 2
# matrix[5,2] = 2
#
# matrix[5,4] = 2
# matrix[5,6] = 2
# matrix[6,3] = 1
# matrix[6,5] = 1
#
# matrix[6,7] = 1
# matrix[7,0] = 1
# matrix[7,2] = 1
# matrix[7,4] = 1
# matrix[7,6] = 1
#
# arr = give_moves(matrix,2)
# print(matrix)
# for i in arr:
#     print(i)
# matrix = calc_state(matrix,arr[0])
# print(matrix)
# m = calc_best_move(matrix,1)
# print(m)
# matrix = calc_state(matrix,m)
# print(matrix)
# m = calc_best_move(matrix,2)
# print(m)
# matrix = calc_state(matrix,m)
# print(matrix)

# print("START GAME!!!")
# print(play()

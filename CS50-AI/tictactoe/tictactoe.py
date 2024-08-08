"""
Tic Tac Toe Player
"""

import math
import copy
import sys

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    xcounter = 0
    ycounter = 0
    for row in board:
        for column in row:
            if column == X:
                xcounter += 1
            elif column == O:
                ycounter += 1
    if ycounter == xcounter:
        return X
    return O



def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    if terminal(board):
        return set()

    possibleActions = set()

    for row in range(len(board)):
        for column in range(len(board[row])):
            if board[row][column] == EMPTY:
                possibleActions.add((row,column))
    return possibleActions



def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    changedBoard = copy.deepcopy(board)
    if 0 <= action[0] <= len(board) and 0 <= action[0] <= len(board[action[0]]) and board[action[0]][action[1]] == EMPTY:
        changedBoard[action[0]][action[1]] = player(board)
        return changedBoard
    raise Exception("Not a vaild location")


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    counter = 0
    #check for if any player has won horizontally
    for row in board:
        startingPlayer = row[0]
        if startingPlayer == EMPTY:
            continue

        for column in row:
            if column == startingPlayer:
                counter += 1
            else:
                break
        if counter == 3:
            return startingPlayer
        counter = 0

    #check for if any player has won vertically
    for column in range(len(board[0])):
        startingPosition = board[0][column]
        if startingPosition == EMPTY:
            continue

        for row in range(len(board)):
            if board[row][column] == startingPosition:
                counter += 1
            else:
                break
        if counter == 3:
            return startingPosition
        counter = 0

    startingPosition = board[0][0]
    if startingPosition != EMPTY:
        for location in range(len(board)):
            if startingPosition == board[location][location]:
                counter += 1
            else:
                break
    if counter == 3:
        return startingPosition
    counter = 0

    boardLen = len(board) - 1
    startingPosition = board[0][boardLen]
    if startingPosition != EMPTY:
        for location in range(len(board)):
            if startingPosition == board[location][boardLen - location]:
                counter += 1
            else:
                break
    if counter == 3:
        return startingPosition
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) != None:
        return True

    for row in board:
        for colmun in row:
            if colmun == EMPTY:
                return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    gameWinner = winner(board)
    if gameWinner == EMPTY:
        return 0
    elif gameWinner == X:
        return 1
    return -1


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # if the game is over then no possible actions can be made
    if terminal(board):
        return None

    bestAction = None
    if player(board) == X:
        bestValue = -10000
        for x in actions(board):
            if bestValue < minValue(result(board, x)):
                bestValue = minValue(result(board, x))
                bestAction = x
    else:
        bestValue = 100
        for x in actions(board):
            if bestValue > maxValue(result(board, x)):
                bestValue = maxValue(result(board, x))
                bestAction = x
    return bestAction

def maxValue(board):
    if terminal(board):
        return utility(board)
    val = -10
    for x in actions(board):
        val = max(val, minValue(result(board, x)))
    return val


def minValue(board):
    if terminal(board):
        return utility(board)

    val = 10
    for x in actions(board):
        val = min(val, maxValue(result(board, x)))
    return val


"""
Tic Tac Toe Player
"""

import math

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
    # implement Counter
    count = {X: 0, O: 0}
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == X:
                count[X] += 1
            elif board[i][j] == O:
                count[O] += 1
    if count[X] == count[O]:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    res = set()
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == EMPTY:
                res.add((i, j))
    return res


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if board[action[0]][action[1]] != EMPTY or action[0] not in range(len(board)) or action[1] not in range(len(board)):
        raise ValueError
    
    res = [row[:] for row in board]
    res[action[0]][action[1]] = player(board)
    return res


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # check rows
    size = len(board)
    for row in range(size):
        if board[row][0] != EMPTY and all(board[row][col] == board[row][0] for col in range(size)):
            return board[row][0]
    # check cols
    for col in range(size):
        if board[0][col] != EMPTY and all(board[row][col] == board[0][col] for row in range(size)):
            return board[0][col]
    # check diagonal
    if board[0][0] != EMPTY and all(board[i][i] == board[0][0] for i in range(size)):
        return board[0][0]
    # check anti-diagonal
    if board[0][size-1] != EMPTY and all(board[i][size-1-i] == board[0][size-1] for i in range(size)):
        return board[0][size-1]
    
    return None
    
        
def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board):
        return True
    size = len(board)
    for i in range(size):
        for j in range(size):
            if board[i][j] == EMPTY:
                return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win = winner(board)
    if win == X:
        return 1
    elif win == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    current_player = player(board)
    
    def max_value(board, alpha, beta):
        if terminal(board):
            return utility(board)
        v = float('-inf')
        for action in actions(board):
            v = max(v, min_value(result(board, action), alpha, beta))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(board, alpha, beta):
        if terminal(board):
            return utility(board)
        v = float('inf')
        for action in actions(board):
            v = min(v, max_value(result(board, action), alpha, beta))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    if current_player == X:
        best_value = float('-inf')
        best_move = None
        alpha = float('-inf')
        beta = float('inf')
        for action in actions(board):
            move_value = min_value(result(board, action), alpha, beta)
            if move_value > best_value:
                best_value = move_value
                best_move = action
            alpha = max(alpha, best_value)
    else:
        best_value = float('inf')
        best_move = None
        alpha = float('-inf')
        beta = float('inf')
        for action in actions(board):
            move_value = max_value(result(board, action), alpha, beta)
            if move_value < best_value:
                best_value = move_value
                best_move = action
            beta = min(beta, best_value)

    return best_move
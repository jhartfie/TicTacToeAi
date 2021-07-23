"""
Tic Tac Toe Player
"""
import copy
import math
import random

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

    x_count = 0
    o_count = 0

    for row in board:
        for cell in row:
            if cell == X:
                x_count += 1
            if cell == O:
                o_count += 1

    if x_count <= o_count:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    possible_actions = set()

    for i in range(0, len(board)):
        for j in range(0, len(board[0])):
            if board[i][j] == EMPTY:
                possible_actions.add((i, j))

    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    new_board = copy.deepcopy(board)
    new_board[action[0]][action[1]] = player(new_board)

    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    # wins = [[(0, 0), (0, 1), (0, 2)],  # 1.1
    #        [(1, 0), (1, 1), (1, 2)],  # 1.2
    #        [(2, 0), (2, 1), (2, 2)],  # 1.3
    #        [(0, 0), (1, 0), (2, 0)],  # 2.1
    #        [(0, 1), (1, 1), (2, 1)],  # 2.2
    #        [(0, 2), (1, 2), (2, 2)],  # 2.3
    #        [(0, 0), (1, 1), (2, 2)],
    #        [(0, 2), (1, 1), (2, 0)]]

    for i in range(0, 3):
        if board[i][0] == X and board[i][1] == X and board[i][2] == X:
            return X
        elif board[i][0] == O and board[i][1] == O and board[i][2] == O:
            return O
    for j in range(0, 3):
        if board[0][j] == X and board[1][j] == X and board[2][j] == X:
            return X
        elif board[0][j] == O and board[1][j] == O and board[2][j] == O:
            return O
    if board[0][0] == X and board[1][1] == X and board[2][2] == X:
        return X
    if board[0][0] == O and board[1][1] == O and board[2][2] == O:
        return O
    if board[0][2] == X and board[1][1] == X and board[2][0] == X:
        return X
    elif board[0][2] == O and board[1][1] == O and board[2][0] == O:
        return O

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    if winner(board) is not None or not actions(board):
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    if winner(board) == X:
        return 1
    if winner(board) == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    # Optimization by hardcoding the first move (the corners are most optimal)
    if board == initial_state():
        randomint = random.randint(0, 3)
        if randomint == 0:
            return 0, 0
        if randomint == 1:
            return 0, 2
        if randomint == 2:
            return 2, 0
        if randomint == 3:
            return 2, 2

    current_player = player(board)
    best_value = float("-inf") if current_player == X else float("inf")

    for action in actions(board):
        new_value = minimax_value(result(board, action), best_value)

        if current_player == X:
            new_value = max(best_value, new_value)

        if current_player == O:
            new_value = min(best_value, new_value)

        if new_value != best_value:
            best_value = new_value
            best_action = action

    return best_action


def minimax_value(board, best_value):
    """
    Returns the best value for each recursive minimax iteration.
    Optimized using Alpha-Beta Pruning: If the new value found is better
    than the best value then return without checking the others.
    """
    if terminal(board):
        return utility(board)

    current_player = player(board)
    value = float("-inf") if current_player == X else float("inf")

    for action in actions(board):
        new_value = minimax_value(result(board, action), value)

        if current_player == X:
            if new_value > best_value:
                return new_value
            value = max(value, new_value)

        if current_player == O:
            if new_value < best_value:
                return new_value
            value = min(value, new_value)

    return value

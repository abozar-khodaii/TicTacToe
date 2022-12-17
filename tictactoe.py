"""
Tic Tac Toe Player
"""
import copy
# import math

X = "X"
O = "O"
EMPTY = None
CENTER = (1, 1)
BEST_STATE = [(0, 0), (0, 2), (2, 0), (2, 2), (1, 1)]


class Node:
    def __init__(self, state, value):
        self.state = state
        self.value = value


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
    x_num = o_num = 0
    for row in board:
        for col in row:
            if col == X:
                x_num += 1
            if col == O:
                o_num += 1
    if x_num == o_num:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    action = set()
    for i in range(0, 3):
        for j in range(0, 3):
            if board[i][j] == EMPTY:
                action.add((i, j))
    return action


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    try:
        result_board = copy.deepcopy(board)
        turn_player = player(result_board)
        if result_board[action[0]][action[1]] != EMPTY:
            raise IndexError(f"action({action[0]}, {action[1]}) not valid index")
        result_board[action[0]][action[1]] = turn_player
        return result_board
    except Exception as e:
        raise ValueError(e)


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # browse horizontally, vertically for winner
    i = 0
    while i <= 2:
        j = 0
        row = board[i][j]
        col = board[j][i]
        if row != EMPTY:
            j += 1
            while j <= 2:
                if row != board[i][j]:
                    break
                if j == 2:
                    return row
                j += 1
        if col != EMPTY:
            j = 1
            while j <= 2:
                if col != board[j][i]:
                    break
                if j == 2:
                    return col
                j += 1
        i += 1
    # browse for winner in diagonally
    center = board[1][1]
    if center == EMPTY:
        return None
    if board[0][0] == center and center == board[2][2]:
        return center
    if board[0][2] == center and center == board[2][0]:
        return center

    #  there is no winner of the game
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    win = winner(board)
    if win == X or win == O:
        return True  # game is over with a winner
    for i in range(0, 3):
        for j in range(0, 3):
            if board[i][j] == EMPTY:
                return False
    return True  # game is over with tie


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    board_winner = winner(board)
    if board_winner == X:
        return 1
    elif board_winner == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    best_node = advance_minimax(board)
    return best_node.state


def advance_minimax(board):
    # current value in circle
    current_player = player(board)
    current_actions = actions(board)

    # end circle call functions if result of action is terminal
    for action in current_actions:
        temp_result = result(board, action)
        if terminal(temp_result):
            return Node(state=action, value=utility(temp_result))

    # call function for current actions
    child_list = []
    for action in current_actions:
        child = advance_minimax(result(board, action))
        #
        if current_player == O and child.value == -1:
            return Node(state=action, value=child.value)
        if current_player == X and child.value == 1:
            return Node(state=action, value=child.value)
        else:
            child_list.append(Node(state=action, value=child.value))

    # find the best node on child list and return
    best_node = child_list[0]
    if current_player == X:
        for child in child_list:
            if child.value > best_node.value:
                best_node = child
            elif child.value == best_node.value:
                if child.state in BEST_STATE and best_node.state != CENTER:
                    best_node = child
        return best_node
    if current_player == O:
        for child in child_list:
            if child.value < best_node.value:
                best_node = child
            elif child.value == best_node.value:
                if child.state in BEST_STATE and best_node.state != CENTER:
                    best_node = child
        return best_node

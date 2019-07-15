# NO IMPORTS!

#############
# Problem 1 #
#############

def ascending_path(graph, start, end):
    visited = set()

    def helper(start, end):
        if start == end:
            return [start]
        visited.add(start)
        for neighbor in graph[start]:
            if neighbor not in visited and neighbor > start:
                path = helper(neighbor, end)
                if path:
                    return [start] + path
        return None

    return helper(start, end)


#############
# Problem 2 #
#############

with open('words2.txt') as f:
    allwords = set(f.read().splitlines())

def is_word(x):
    return x in allwords

def split_words(x):
    raise NotImplementedError # reserved for Quiz 3 practice


#############
# Problem 3 #
#############

##
## Problem 3A
##

def game_status(board):
    """Return 'X' if X has three in a row; 'O' if X does not have three in
       a row but O does; '-" if neither has won but the game is still
       in progress; or 'T' if the game is over but ends in a tie where
       neither player has three in a row.

    """
    trios = [get_row(board, r) for r in range(3)] + \
            [get_col(board, c) for c in range(3)] + \
            [get_diag(board, d) for d in range(2)]
    for trio in trios:
        if is_trio_winner(trio, 'X'):
            return 'X'
    for trio in trios:
        if is_trio_winner(trio, 'O'):
            return 'O'
    return '-' if '-' in board else 'T'

def is_trio_winner(trio, p):
    """Return True if player p is a winner of the trio"""
    return all(trio[i] == p for i in range(3))

def get_row(board, r):
    return board[r*3: (r+1)*3]

def get_col(board, c):
    return board[c] + board[c+3] + board[c+6]

def get_diag(board, d):
    if d == 0:
        return board[0] + board[4] + board[8]
    else:
        return board[2] + board[4] + board[6]

##
## Problem 3B
##

def forced_win(board):
    # Check if game is already over
    win = game_status(board)
    if win == 'X':
        return -1
    elif win != '-':
        return None

    # Find a location for X, such that we still have a forced_win for
    # every responding placement of an O.
    for X_square in empty_squares(board):
        new_board = set_square(board, X_square, 'X');

        # Check for an immediate win or loss/tie
        win = game_status(new_board)
        if win == 'X':
            return X_square
        elif win != '-':
            continue

        # See if can force a win for every responding O move
        win_for_all_O = True
        for O_square in empty_squares(new_board):
            next_board = set_square(new_board, O_square, 'O')
            wins = forced_win(next_board)
            if wins is None:
                win_for_all_O = False
                break
        if win_for_all_O:
            # Forced a win for this square!
            return X_square

    # Nothing worked; oh well
    return None

def empty_squares(board):
    """yield square labels for empty squares in board"""
    for square in range(9):
        if board[square] == '-':
            yield square

def set_square(board, square, p):
    return board[0:square] + p + board[square+1:]

# If we wanted to get ALL winning moves...
def all_forced_wins(board, player='X'):
    # X wins by winning; O "wins" by winning or tieing
    opponent = 'O' if player == 'X' else 'X'
    win = game_status(board)
    if win == player:
        return set()
    elif win == opponent:
        return None
    elif win == 'T':
        if player=='O':
            return set()
        else:
            return None

    winning_moves = {p for p in empty_squares(board) \
                       if all_forced_wins(set_square(board, p, player), opponent) is None}
    return winning_moves if winning_moves else None


if __name__ == "__main__":
    pass
    
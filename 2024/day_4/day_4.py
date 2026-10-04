"""
Structure will be lists of nested lists, where each nested list is a row of the board
"""

def get_indices(idx, word_length, reverse=False):
    if reverse:
        ending_idx = idx + 1
        starting_idx = ending_idx - word_length
    else:
        starting_idx = idx
        ending_idx = starting_idx + word_length
    return starting_idx, ending_idx

def is_word_horizontal(row_idx, col_idx, reverse=False, word='XMAS'):
    """
    Returns a boolean if the word is present in the direction stipulated
    reverse flag should be set to True if we want to search right to left
    Otherwise, reverse of False if we want to search left to right
    """
    starting_idx, ending_idx = get_indices(col_idx, len(word), reverse)
    word_candidate = board[row_idx][starting_idx:ending_idx]
    return word_candidate == word or ''.join(reversed(word_candidate)) == word

def is_word_vertical(row_idx, col_idx, reverse=False, word='XMAS'):
    """
    Returns a boolean if the word is present in the direction stipulated
    reverse flag should be set to True if we want to search bottom to top
    Otherwise, reverse of False if we want to search top to bottom
    """
    starting_idx, ending_idx = get_indices(row_idx, len(word), reverse)
    word_candidate = ''.join([row[col_idx] for row in board[starting_idx:ending_idx]])
    return word_candidate == word or ''.join(reversed(word_candidate)) == word

def is_word_diagonal(row_start, col_start, horizontal_reverse=False, vertical_reverse=False, word='XMAS'):
    """
    Returns a boolean if the word is present in the direction stipulated
    """
    word_candidate = []
    horizontal_factor = -1 if horizontal_reverse else 1
    vertical_factor = -1 if vertical_reverse else 1
    max_col = len(board[0]) - 1
    max_row = len(board) - 1

    for offset in range(0, len(word)):
        row_idx = row_start + offset * vertical_factor
        col_idx = col_start + offset * horizontal_factor

        if (row_idx >= 0 and row_idx <= max_row) and (col_idx >= 0 and col_idx <= max_col):
            word_candidate.append(board[row_idx][col_idx])

    return ''.join(word_candidate) == word or ''.join(reversed(word_candidate)) == word

# **************************************************************************************

# Read in board
with open('day_4.txt', 'r') as file:
    board = file.readlines()
board = [row.strip() for row in board]

count = 0
for idx_row, row in enumerate(board):
    for idx_col, letter in enumerate(row):
        if letter != 'X':
            continue

        count += is_word_horizontal(idx_row, idx_col)
        count += is_word_horizontal(idx_row, idx_col, reverse=True)

        count += is_word_vertical(idx_row, idx_col)
        count += is_word_vertical(idx_row, idx_col, reverse=True)

        count += is_word_diagonal(idx_row, idx_col)
        count += is_word_diagonal(idx_row, idx_col, horizontal_reverse=True)
        count += is_word_diagonal(idx_row, idx_col, horizontal_reverse=False, vertical_reverse=True)
        count += is_word_diagonal(idx_row, idx_col, horizontal_reverse=True, vertical_reverse=True)

print(count) # Part 1 complete





def is_x_mas(row_center, col_center):
    """
    Returns a boolean if the X spells MAS for both diagonals
    row_center and col_center pertain to the coordinates of the middle A
    """
    max_col = len(board[0]) - 1
    max_row = len(board) - 1

    if row_center < 1 or row_center > max_row - 1 or col_center < 1 or col_center > max_col - 1:
        return False

    # diagonal1 is diagonal from top left to bottom right
    # diagonal2 is diagonla from bottom left to top right
    diagonal1 = ''
    diagonal2 = ''
    for offset in range(-1, 2):
        diagonal1 += board[row_center + offset][col_center + offset]
        diagonal2 += board[row_center - offset][col_center + offset]

    return (diagonal1 == 'MAS' or diagonal1 == 'SAM') and (diagonal2 == 'MAS' or diagonal2 == 'SAM')

count = 0
for idx_row, row in enumerate(board):
    for idx_col, letter in enumerate(row):
        if letter != 'A':
            continue
        count += is_x_mas(idx_row, idx_col)

print(count) # Part 2 complete
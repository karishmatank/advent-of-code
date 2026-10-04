"""
My first attempt wasn't super elegant, so I'm trying again. Especially part 1
"""

DIRECTIONS_FACTORS = {
    'h_left_to_right': {
        'row': 0,
        'col': 1
    },
    'h_right_to_left': {
        'row': 0,
        'col': -1
    },
    'v_top_to_bottom': {
        'row': 1,
        'col': 0
    },
    'v_bottom_to_top': {
        'row': -1,
        'col': 0
    },
    'd_up_right': {
        'row': -1,
        'col': 1
    },
    'd_up_left': {
        'row': -1,
        'col': -1
    },
    'd_down_right': {
        'row': 1,
        'col': 1
    },
    'd_down_left': {
        'row': 1,
        'col': -1
    }
}


def count_words(row_start, col_start, target='XMAS'):
    """
    Counts all words in horizontal, vertical, and diagonal directions from the starting point
    that match the target word
    """
    count = 0

    max_col = len(board[0]) - 1
    max_row = len(board) - 1

    for factors in DIRECTIONS_FACTORS.values():
        candidate_word = ''

        for offset in range(len(target)):
            row_idx = row_start + offset * factors['row']
            col_idx = col_start + offset * factors['col']

            # If the indices are in bounds, add the letter to the candidate word
            # Else, end early- we won't get to the target word
            if (0 <= row_idx <= max_row) and (0 <= col_idx <= max_col):
                candidate_word += board[row_idx][col_idx]
            else:
                break

            # Check to see whether candidate word has veered from target early
            # If so, no use checking the rest of the letters
            if (candidate_word != target[0:len(candidate_word)]):
                break

        if candidate_word == target:
            count += 1

    return count

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

        count += count_words(idx_row, idx_col)

print(count) # Part 1 complete



# Part 2 is fine from before, so I won't redo it
ROLL_ICON = "@"
EMPTY_ICON = "."

with open("day_4.txt") as file:
    data = file.readlines()

data = [i.replace("\n", "") for i in data]

# Turn each row into a list. Entire thing will now be a nested list
# Makes it easier for part 2 to mutate data to remove rolls
data = [list(row) for row in data]

total_col = len(data[0])
total_row = len(data)

# If total_row is first, look towards current and next row
# If total_row is last, look towards last and current row
# If total_col is first, look towards current and next col
# If total_col is last, look towards last and current col

first_row_idx = 0
last_row_idx = len(data) - 1
first_col_idx = 0
last_col_idx = len(data[0]) - 1

def get_surrounding_squares(idx_row, idx_col):
    surrounding_squares = []

    min_row = max(first_row_idx, idx_row - 1)
    max_row = min(last_row_idx, idx_row + 1)
    min_col = max(first_col_idx, idx_col - 1)
    max_col = min(last_col_idx, idx_col + 1)

    for check_row in range(min_row, max_row + 1):
        for check_col in range(min_col, max_col + 1):

            if check_row == idx_row and check_col == idx_col:
                continue

            surrounding_squares.append(data[check_row][check_col])

    return surrounding_squares

def remove_rolls(roll_idxs):
    for pair in roll_idxs:
        idx_row, idx_col = pair
        data[idx_row][idx_col] = EMPTY_ICON


# Part 2: Keep identifying and removing rolls of paper until we can't remove any more
total_moved = 0

while True:
    num_rolls_movable = 0
    roll_idxs_to_move = []

    for idx_row in range(total_row):
        for idx_col in range(total_col):
            # Get current square, check if it has a roll
            current_square = data[idx_row][idx_col]
            if current_square != ROLL_ICON:
                continue
            
            # Get the relevant data points around the current square
            surrounding_squares = get_surrounding_squares(idx_row, idx_col)

            # Count roll if there are < 4 rolls in surrounding squares
            # Record current idx_row and idx_col as well to remove roll in the future
            if surrounding_squares.count(ROLL_ICON) < 4:
                num_rolls_movable += 1
                roll_idxs_to_move.append((idx_row, idx_col))
    
    if num_rolls_movable == 0:
        break

    total_moved += num_rolls_movable

    # Mutate data to remove the rolls we identified
    remove_rolls(roll_idxs_to_move)


print(total_moved)
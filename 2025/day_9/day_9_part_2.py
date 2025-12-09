def calc_area(coord1, coord2):
    x1, y1 = coord1
    x2, y2 = coord2

    x_dist = abs(x2 - x1) + 1
    y_dist = abs(y2 - y1) + 1
    return x_dist * y_dist

def is_on_same_row(coord1, coord2):
    _, y1 = coord1
    _, y2 = coord2

    return y1 == y2

def is_on_same_col(coord1, coord2):
    x1, _ = coord1
    x2, _ = coord2

    return x1 == x2

def fill_green_tiles_between(coord1, coord2):
    x1, y1 = coord1
    x2, y2 = coord2

    # For each of the for loops below, I am deliberately overwriting any # tiles to be X
    # with my choice of start and end for the ranges
    # Ultimately, it doesn't matter whether the tile is red or green, it just matters that we can include it
    if is_on_same_row(coord1, coord2):
        # y1 and y2 are the same
        for idx_col in range(min(x1, x2), max(x1, x2) + 1):
            grid[y1][idx_col] = 'X'
    elif is_on_same_col(coord1, coord2):
        # x1 and x2 are the same
        for idx_row in range(min(y1, y2), max(y1, y2) + 1):
            grid[idx_row][x1] = 'X'
    
def is_rect_all_filled(coord1, coord2):
    x1, y1 = coord1
    x2, y2 = coord2

    # Get squares from within rectangle
    squares = []
    for idx_row in range(min(y1, y2), max(y1, y2) + 1):
        squares.extend(grid[idx_row][min(x1, x2): max(x1, x2) + 1])
    
    return all(sq == 'X' for sq in squares)

        


# Read in data

# red_tiles = []

# with open("day_9.txt", 'r') as file:
#     for line in file:
#         line = [int(coord) for coord in line.strip().split(',')]
#         red_tiles.append(tuple(line))


red_tiles = [
    (7,1),
    (11,1),
    (11,7),
    (9,7),
    (9,5),
    (2,5),
    (2,3),
    (7,3)
]


# Create grid
max_x = max(tile[0] for tile in red_tiles)
max_y = max(tile[1] for tile in red_tiles)

# Place red tiles as #
grid = [["." for _ in range(max_x + 1)] for _ in range(max_y + 1)]
for red_tile in red_tiles:
    x, y = red_tile
    grid[y][x] = '#'

# Fill in green tiles between red with X. Fills only if they are in same row or col
for idx1 in range(len(red_tiles)):
    for idx2 in range(idx1 + 1, len(red_tiles)):
        tile1 = red_tiles[idx1]
        tile2 = red_tiles[idx2]
        fill_green_tiles_between(tile1, tile2)

# Fill in green tiles between newly placed green tiles, per row
# For each row, check to see if there are any '.' between 'X'

for idx_row, row in enumerate(grid):
    # Check if there are '.' between any 'X'
    row_str = "".join(row)
    ex_outer_periods = row_str.strip('.')
    if '.' in ex_outer_periods:
        # In this case, we need to fill the '.' with 'X'
        # Find indices of first and last X
        first_x = row_str.find('X')
        last_x = row_str.rfind('X')
        fill_green_tiles_between((first_x, idx_row), (last_x, idx_row))



# Find the max_area, using the red tile coordinates
# For each pair of coordinates, get each square in the rectangle formed
# If each square is a 'X' (we've already overwritten the '#' to 'X'), then its area counts
# Otherwise, skip and go to the next pair of coordinates

max_area = 0

for idx_corner1 in range(len(red_tiles)):
    for idx_corner2 in range(idx_corner1 + 1, len(red_tiles)):
        corner1 = red_tiles[idx_corner1]
        corner2 = red_tiles[idx_corner2]

        area = calc_area(corner1, corner2)
        if area > max_area and is_rect_all_filled(corner1, corner2):
            max_area = area

print(max_area) # Part 2 incomplete, works well with small example, takes very long with full dataset

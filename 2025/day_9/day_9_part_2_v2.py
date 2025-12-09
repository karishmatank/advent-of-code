# Going to try again without creating the grid
# Will trace the edges and find whether a given coordinate's x and y is within the trace
# Optimizations made:
# 1. Used a set to store each of the edge coordinates, instead of creating the grid and storing every single cell
# 2. Created a dictionary where each key is a row index # and each value is a list that has the min and max col index # of that row
# 3. Simplified is_rect_all_filled- Instead of going cell by cell, I go through each row and check if the col indices
#    for the rectangle are in bounds for the polygon formed by the edge coordinates for that row. This is where the dictionary
#    helps as I was previously checking each cell and doing the computation over again for each cell.

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

def add_green_tiles(coord1, coord2):
    x1, y1 = coord1
    x2, y2 = coord2

    # For each of the for loops below, I am deliberately overwriting any # tiles to be X
    # with my choice of start and end for the ranges
    # Ultimately, it doesn't matter whether the tile is red or green, it just matters that we can include it
    if is_on_same_row(coord1, coord2):
        # y1 and y2 are the same
        for idx_col in range(min(x1, x2), max(x1, x2) + 1):
            edge_coordinates.add((idx_col, y1))
    elif is_on_same_col(coord1, coord2):
        # x1 and x2 are the same
        for idx_row in range(min(y1, y2), max(y1, y2) + 1):
            edge_coordinates.add((x1, idx_row))
    
def is_rect_all_filled(coord1, coord2):
    x1, y1 = coord1
    x2, y2 = coord2

    # Don't iterate over every coordinate anymore! 
    x_range = [min(x1, x2), max(x1, x2)]
    y_range = [min(y1, y2), max(y1, y2)]

    for row in range(min(y_range), max(y_range) + 1):
        edges_x = edge_cols_per_row[row]
        if min(x_range) < min(edges_x) or max(x_range) > max(edges_x):
            return False
    
    return True
    
# Read in data

red_tiles = []

with open("day_9.txt", 'r') as file:
    for line in file:
        line = [int(coord) for coord in line.strip().split(',')]
        red_tiles.append(tuple(line))


# red_tiles = [
#     (7,1),
#     (11,1),
#     (11,7),
#     (9,7),
#     (9,5),
#     (2,5),
#     (2,3),
#     (7,3)
# ]

# We'll fill the green tiles in here too
edge_coordinates = set(red_tiles)

# Fill in green tiles between red with X to make up the edges of the polygon. Fills only if they are in same row or col
for idx1 in range(len(red_tiles)):
    for idx2 in range(idx1 + 1, len(red_tiles)):
        tile1 = red_tiles[idx1]
        tile2 = red_tiles[idx2]
        if is_on_same_col(tile1, tile2) or is_on_same_row(tile1, tile2):
            add_green_tiles(tile1, tile2)


# Create a dictionary that maps each row # to the min and max col #s
# This will make it easier for us to search through each coordinate of a rectangle candidate to check if the
# rectangle is valid later on
# Essentially does all the work up front to check min and max rather than leaving it to each iteration
min_y = min(tile[1] for tile in red_tiles)
max_y = max(tile[1] for tile in red_tiles)

edge_cols_per_row = dict()
for coord in edge_coordinates:
    x, y = coord
    current_min_max_per_row = edge_cols_per_row.get(y, [])
    if not current_min_max_per_row:
        edge_cols_per_row[y] = [x, x]
    else:
        new_min = x if x < current_min_max_per_row[0] else current_min_max_per_row[0]
        new_max = x if x > current_min_max_per_row[1] else current_min_max_per_row[1]
        edge_cols_per_row[y] = [new_min, new_max]


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

print(max_area) # Part 2 complete!!!!

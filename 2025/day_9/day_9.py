def calc_area(coord1, coord2):
    x1, y1 = coord1
    x2, y2 = coord2

    x_dist = abs(x2 - x1) + 1
    y_dist = abs(y2 - y1) + 1
    return x_dist * y_dist


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

max_area = 0

for idx_corner1 in range(len(red_tiles)):
    for idx_corner2 in range(idx_corner1 + 1, len(red_tiles)):
        corner1 = red_tiles[idx_corner1]
        corner2 = red_tiles[idx_corner2]

        area = calc_area(corner1, corner2)

        if area > max_area:
            max_area = area

print(max_area) # Part 1 complete
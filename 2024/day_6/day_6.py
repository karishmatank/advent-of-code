"""
Current location of the map = ^ sign. We'll represent as coordinates where the first coordinate is row idx, second is col idx

Move up = decrease idx number until you get to the min idx number (0) or an obstacle (#). Then you're at an edge
Move down = increase idx number until you get to the max idx number (length of board) or an obstacle (#)
Move right = increase col number until you get to the max idx number (length of a board row) or an obstacle (#)
Move left = decrease idx number until we get to the min idx number (0) or an obstacle (#)

Count the number of free positions between current position and an obstacle or edge, add that to a total counter

While the current location is not at an edge:
    - Move in the direction you are facing until you can't anymore (get to the edge or an obstacle)
    - If we are at the edge:
        - Done
    - If at an obstacle:
        - Change direction
        - Repeat above steps

Are we at an edge?
- Get coordinates for next step in the current direction
- If new row position is 0 or max idx number (length of board), yes
- OR If new col position is 0 or max idx number (length of a board row), yes

Are we at an obstacle?
- IF the next step in the current direction is '#', yes
- Otherwise, no

Change direction
- If 'up', change to 'right'
- If 'right', change to 'down'
- If 'down', change to 'left'
- If 'left', change to 'up'

Move in the direction you are facing until you can't anymore
- While we are not at the edge or the next step isn't an obstacle:
    - Move one step in the direction
    - Update current location with the new coordinates
    - If we haven't already visited the new square
        - Mark the new location with an 'X'
        - Increment visited spaces counter
- Return

"""

import copy

class Board:
    OBSTACLE_MARKER = '#'
    VISITED_MARKER = 'X'
    NOT_VISITED_MARKER = '.'
    INITIAL_POS_MARKER = '^'
    DIRECTIONS = {
        'up': [-1, 0],
        'right': [0, 1],
        'down': [1, 0],
        'left': [0, -1]
    }

    def __init__(self, map):
        self.map = copy.deepcopy(map)
        self.visited_spaces = 1 # Start with current position
        self.direction_idx = 0
        self.initial_position = tuple(self.get_initial_position())
        self.position = list(self.initial_position)
        self.mark_initial_position()
        self.hit_obstacles_at = set()

        self.min_row_idx = 0
        self.max_row_idx = len(self.map) - 1
        self.min_col_idx = 0
        self.max_col_idx = len(self.map[0]) - 1

    def get_initial_position(self):
        for row_idx, row in enumerate(self.map):
            if Board.INITIAL_POS_MARKER in row:
                col_idx = row.index(Board.INITIAL_POS_MARKER)
                return [row_idx, col_idx]
        raise Exception('No initial position')

    def move(self):
        while True:
            self.move_in_direction()
            if self.at_edge():
                break
            if self.at_obstacle():
                self.change_direction()

    def is_loop_present(self):
        while True:
            self.move_in_direction()
            if self.at_edge():
                return False
            if self.at_obstacle():
                if self.have_seen_obstacle():
                    return True
                else:
                    self.hit_obstacles_at.add(tuple([tuple(self.position), self.direction_idx]))
                    self.change_direction()

    def at_edge(self):
        next_row, next_col = self.get_next_step()
        return (next_row < self.min_row_idx or next_row > self.max_row_idx) or \
               (next_col < self.min_col_idx or next_col > self.max_col_idx)

    def move_in_direction(self):
        while not self.at_edge() and not self.at_obstacle():
            self.position = self.get_next_step()
            if not self.is_current_square_visited():
                self.mark_current_square()
                self.visited_spaces += 1

    def at_obstacle(self):
        next_row, next_col = self.get_next_step()
        return self.map[next_row][next_col] == Board.OBSTACLE_MARKER

    def change_direction(self):
        self.direction_idx = (self.direction_idx + 1) % len(Board.DIRECTIONS.keys())

    def get_next_step(self):
        match self.direction_idx:
            case 0:
                movement = Board.DIRECTIONS['up']
            case 1:
                movement = Board.DIRECTIONS['right']
            case 2:
                movement = Board.DIRECTIONS['down']
            case 3:
                movement = Board.DIRECTIONS['left']
            case _:
                raise Exception('Invalid direction index')

        return [x + y for x, y in zip(self.position, movement)]

    def is_current_square_visited(self):
        current_row, current_col = self.position
        return self.map[current_row][current_col] == Board.VISITED_MARKER

    def mark_current_square(self):
        current_row, current_col = self.position
        self.map[current_row][current_col] = Board.VISITED_MARKER

    def mark_initial_position(self):
        self.mark_current_square()

    def get_visited_coordinates(self):
        if self.visited_spaces <= 1:
            self.move()

        path = set()
        for idx_row, row in enumerate(self.map):
            for idx_col, col in enumerate(row):
                coordinates = (idx_row, idx_col)
                if col == Board.VISITED_MARKER and coordinates != self.initial_position:
                    path.add(coordinates)
        return path

    def have_seen_obstacle(self):
        return tuple([tuple(self.position), self.direction_idx]) in self.hit_obstacles_at

# Read in data
with open('day_6.txt', 'r') as file:
    data = file.readlines()
data = [list(row.strip()) for row in data]

board = Board(data)
board.move()
print(board.visited_spaces) # Part 1 complete!





"""
How do we know we are in a loop?
- If we've seen an obstacle before from a specific "vantage point" (specific coordinate), then we're in a loop
because there is only one way to go from that vantage point, so we'll just keep repeating our path
- EDIT: This is actually not true- we can arrive at an obstacle from one direction, turn to the right, and not be
able to move anywhere else because the next step has an obstacle. So we need the direction we came from as well

Create a simulation:
- Each simulation creates a new board that starts at the original state
- Each simulation places a new obstacle at a particular location
    - The obstacles should only be placed in locations where we determined the guard visited in part 1
    - No need to place an obstacle in every unique location on the board
- For each simulation with the new obstacle:
    - If we reach an obstacle, and we have already visited that location before in the same direction we're travelling in,
      we are in a loop


Board class:
- Init
    - Record initial starting position separate from self.position
    - Create new set `hit_obstacles_at`
        - Members are tuples of 1) nested tuples of coordinates we've visited where we hit obstacles
          and 2) the direction index we've reached coordinate from (0, 1, 2, or 3) representing what direction we were travelling in
- `is_loop_present` method
    - While we are not about to move off the board:
        - Move in the current direction as far as possible
        - If you're then at the edge (and about to hop off the grid on the next step):
            - We're done, no loop
        - If we're at an obstacle
            - Check the map to see we've previously been at our current coordinate w/ current direction (`have_seen_obstacle`)
            - If so:
                - We're done, loop detected
            - Else:
                - Add current position and direction index to `hit_obstacles_at`
                - Change direction and keep going
- Get list of coordinates along guard path (`get_coordinates`)
    - If `visited_spaces` <= 1:
        - Run the `move` method
    - Create a new set -> `path`
    - For each coordinate in `map`:
        - If its marker is an 'X' and coordinates don't match initial starting position:
            - Record the row and column in a tuple and add to `path`
    - Return `path`
- Check if we've seen the current obstacle at our position -> `have_seen_obstacle`
    - True if current position and direction idx combo is in `hit_obstacles_at`

Simulation class:
- State
    - Number of locations that create loops (init to 0) -> `loop_count`
    - Original map
    - List of coordinates along guard path (as per part 1) -> `path`
        - Create a new instance of board with the original map
        - Call `get_coordinates`
- Start simulation:
    - For each coordinate in `path`:
        - Duplicate the map and add an obstacle at the coordinate
        - Create new instance of Board using the new map -> `board`
        - Check if the new obstacle causes a loop -> `is_loop_present` on `board`
        - If so
            - Increment `loop_count` by 1

"""

class Simulation:
    def __init__(self, map):
        self.loop_count = 0
        self.map = map
        self.path  = Board(map).get_visited_coordinates()

    def start(self):
        for idx_row, idx_col in self.path:
            new_map = copy.deepcopy(self.map)
            new_map[idx_row][idx_col] = Board.OBSTACLE_MARKER

            board = Board(new_map)
            if board.is_loop_present():
                self.loop_count += 1

sim = Simulation(data)
sim.start()

print(sim.loop_count) # Part 2 complete!

"""
The solution above is a bit slow. How can we improve?
- copy.deepcopy is probably not necessary
- May be a more efficient way to move much faster through a grid instead of going step by step
"""
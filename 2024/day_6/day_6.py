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
        self.map = map
        self.visited_spaces = 1 # Start with current position
        self.direction_idx = 0
        self.position = self.get_initial_position()
        self.mark_initial_position()

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



# Read in data
with open('day_6.txt', 'r') as file:
    data = file.readlines()
data = [list(row.strip()) for row in data]

board = Board(data)
board.move()
print(board.visited_spaces) # Part 1 complete!
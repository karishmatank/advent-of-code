# Rewriting code to be cleaner

class Grid:
    def __init__(self):
        self._initialize_grid()

    def _initialize_grid(self):
        """Read in grid data"""
        with open("../../data/day_4.txt") as file:
            data = file.readlines()

        data = [row.replace("\n", "") for row in data]
        self.data = [[Square(space) for space in row] for row in data]

    @property
    def total_col(self):
        """Get total columns in grid"""
        return len(self.data[0])
    
    @property
    def total_row(self):
        """Get total rows in grid"""
        return len(self.data)
    
    def _get_surrounding_squares(self, idx_row, idx_col):
        """Get 8 surrounding squares for the current indices. Current indices may map to edge or corner."""
        surrounding_squares = []

        min_row_idx = max(0, idx_row - 1) # First row idx is always 0
        max_row_idx = min(self.total_row - 1, idx_row + 1)
        min_col_idx = max(0, idx_col - 1) # First col idx is always 0
        max_col_idx = min(self.total_col - 1, idx_col + 1)

        for check_row in range(min_row_idx, max_row_idx + 1):
            for check_col in range(min_col_idx, max_col_idx + 1):
                
                # Don't count current square
                if check_row == idx_row and check_col == idx_col:
                    continue

                surrounding_squares.append(self.data[check_row][check_col])

        return surrounding_squares
    
    def _is_square_movable(self, idx_row, idx_col):
        """Check if square is surrounded by fewer than 4 rolls"""
        surrounding_icons = [square.icon for square in self._get_surrounding_squares(idx_row, idx_col)]
        return surrounding_icons.count(Square.ROLL_ICON) < 4
    
    def identify_rolls_to_move(self):
        """Return a list of indices where we will need to remove rolls"""
        roll_idxs_to_move = []

        for idx_row in range(self.total_row):
            for idx_col in range(self.total_col):
                # Get current square, check if it has a roll
                current_square = self.data[idx_row][idx_col]
                if not current_square.is_roll:
                    continue
                
                # Count roll if there are < 4 rolls in surrounding squares
                if self._is_square_movable(idx_row, idx_col):
                    roll_idxs_to_move.append((idx_row, idx_col))

        return roll_idxs_to_move
    
    def move_roll(self, idx_row, idx_col):
        """Remove the roll at the specified indices"""
        square = self.data[idx_row][idx_col]
        square.remove_roll()

    
class Square:
    ROLL_ICON = "@"
    EMPTY_ICON = "."

    def __init__(self, icon):
        self.icon = icon

    @property
    def is_roll(self):
        """Does the square have a roll?"""
        return self.icon == Square.ROLL_ICON

    def remove_roll(self):
        """Change icon to remove roll"""
        self.icon = Square.EMPTY_ICON


class Simulation:
    def __init__(self):
        self.total_moved = 0
        self.grid = Grid()

    def run(self):
        """Keep running until there are no rolls to move"""
        while True:
            roll_idxs_to_move = self.grid.identify_rolls_to_move()

            if len(roll_idxs_to_move) == 0:
                break
            
            self.total_moved += len(roll_idxs_to_move)

            # Mutate grid to remove the rolls we identified
            for pair_row, pair_col in roll_idxs_to_move:
                self.grid.move_roll(pair_row, pair_col)
                

simulation = Simulation()
simulation.run()
print(simulation.total_moved)
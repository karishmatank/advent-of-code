class Dial:
    MAX_POS = 99
    MIN_POS = 0
    TOTAL_SPACES = MAX_POS - MIN_POS + 1

    def __init__(self):
        self.initialize_position()
        self.document = Document('../../data/day_1.txt')
        self._count_zero = 0

    def initialize_position(self):
        """Dial starts pointing at 50"""
        self._position = 50

    def _get_next_rotation(self):
        """Helper function to extract next rotation"""
        try:
            instruction = self.document.next_rotation
        except StopIteration:
            return None
        return instruction
        
    def _extract_rotation_info(self, info):
        direction = info[0]
        num_spaces = int(info[1:])
        return (direction, num_spaces)
    
    def rotate(self):
        """Rotate dial based on direction and number of spaces"""
        instruction = self._get_next_rotation()
        
        try:
            direction, num_spaces = self._extract_rotation_info(instruction)
        except TypeError:
            return 0

        if direction == 'L':
            new_pos = self._position - num_spaces
        else:
            new_pos = self._position + num_spaces

        # Part 2- Record number of times it passes 0 as well
        self._check_passed_zero(direction, new_pos)

        # Part 1- Check if it dial lands on zero
        self._position = new_pos % Dial.TOTAL_SPACES
        self._check_position_zero()
        return 1

    def _check_position_zero(self):
        """Check if position is zero. If so, increment internal counter"""
        if self._position == 0:
            self._count_zero += 1

    def _check_passed_zero(self, direction, new_pos):
        """Record the number of times the dial passed zero while rotating"""
        start = self._position
        
        if direction == 'L':
            # We rotate left (towards lower numbers)
            # We won't count the actual last step here (we deliberately exclude the end)
            # So that if it lands on 0, we count that later as part of _check_position_zero
            # Likewise, we start at one step before start so that we don't include a 0 if we started at 0
            steps = range(start - 1, new_pos, -1)
        else:
            # We rotate right (towards higher numbers)
            steps = range(start + 1, new_pos)
        
        steps_normalized = [step % Dial.TOTAL_SPACES for step in steps]
        self._count_zero += steps_normalized.count(0)

    @property
    def num_zero_positions(self):
        return self._count_zero

class Document:
    def __init__(self, file):
        self.load_data(file)

    def load_data(self, file):
        """Read in data""" 
        with open(file, 'r') as f:
            data = f.readlines()

        data = (turn.replace("\n", "") for turn in data)
        self._rotations = data

    @property
    def next_rotation(self):
        return next(self._rotations)
    

if __name__ == "__main__":
    dial = Dial()
    while True:
        success = dial.rotate()
        if not success:
            break

    print(dial.num_zero_positions) # Passed day 1 parts 1 and 2

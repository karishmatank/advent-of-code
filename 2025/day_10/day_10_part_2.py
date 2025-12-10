"""
Quick algo for getting fewest presses:
- For each combo
    - Represent each button as a list i.e. (3) => [0, 0, 0, 1] or (1, 3) => [0, 1, 0, 1]
    - Have to try to do some sort of linear combo exercise to figure out what freq of buttons gets us the joltage
    - Record the total # of presses required (sum of presses per button) for each combo
- Across combos, record the min # as you go
- Return that min number

Issue is that it seems we can't solve this using linear algebra, as we need A to be square to use the numpy functionality.
    - A = each button is a column
    - x = solve for this
    - b = joltage
A likely won't be square, as we have combos that have different #s of buttons, so joltage length not necessarily = to
# of buttons.

So I'll leave it here for part 2 then...

"""
from itertools import combinations
import numpy as np


def get_all_combinations(buttons):
    """Return list should already be sorted by length"""
    return [combo for i in range(1, len(buttons) + 1) for combo in list(combinations(buttons, i))]

def button_to_list(button, total_elements):
    lst = [0] * total_elements
    for idx in button:
        lst[idx] = 1
    return lst


def get_fewest_presses(target_joltage, combos):
    for combo in combos:
        current_joltage = [0] * len(target_joltage)
        
        # Represent each button in the combo as a list
        buttons = [button_to_list(button, len(target_joltage)) for button in combo]
        
        # Solve system of equations
        A = np.array(buttons)
        b = np.array(target_joltage)
        print(A)
        print(b)


        x = np.linalg.solve(A, b)




# Sample data
data = "[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}"

sum_button_presses = 0

# with open('day_10.txt', 'r') as file:
#     for line in file:
target_light_diagram, *buttons, joltage = data.strip().split()
buttons = [tuple(map(int, button[1:-1].split(","))) for button in buttons]
joltage = [int(num) for num in joltage[1:-1].split(",")]

# Get all combinations
combos = get_all_combinations(buttons)
get_fewest_presses(joltage, combos)
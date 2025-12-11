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

I came back to try to use np.linalg.pinv to solve for the least squares solution, which theoretically works for non-square As
but it's not guaranteed to converge + rounding up/down the solution isn't guaranteed to be correct. 
It worked for the test cases but not for the input.

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
    min_presses = None

    for combo in combos:
        current_joltage = [0] * len(target_joltage)
        # print(combo)
        
        # Represent each button in the combo as a list
        buttons = [button_to_list(button, len(target_joltage)) for button in combo]
        
        # Solve system of equations
        A = np.array(buttons).T
        b = np.array(target_joltage).T
        # print(A)
        # print(b)

        x = np.linalg.pinv(A) @ b

        # We round because the solutions are not guaranteed to be integers
        x = [round(num) for num in list(x)]

        # print(buttons)
        # print(x)

        # Check that solution doesn't have weird negative values
        if not all(num > 0 for num in x):
            continue
        
        # Check that if we press each button the specified number of times (as listed in x), we actually get the joltage
        # we want
        lists_to_add = []
        for idx in range(len(x)):
            lists_to_add.append([num * x[idx] for num in buttons[idx]])

        current_joltage = [sum(elements) for elements in zip(*lists_to_add)]
        if current_joltage != target_joltage:
            continue

        if not min_presses or sum(x) < min_presses:
            # current_min_combo = combo
            min_presses = sum(x)
    
    # print(combo)
    # print(min_presses)
    return min_presses




# Sample data
line = "[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}"
# line = "[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}"
# line = "[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"

# For each of the above, answers are 10, 12, 11

sum_button_presses = 0

# with open('day_10.txt', 'r') as file:
#     for line in file:
target_light_diagram, *buttons, joltage = line.strip().split()
buttons = [tuple(map(int, button[1:-1].split(","))) for button in buttons]
joltage = [int(num) for num in joltage[1:-1].split(",")]

# Get all combinations
combos = get_all_combinations(buttons)
sum_button_presses += get_fewest_presses(joltage, combos)

print(sum_button_presses) # Works with the test cases, but for at least one of the input lines, doesn't converge for any combo
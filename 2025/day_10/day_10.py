"""
Some observations:
1. We should only press a button zero or one times. Pressing it 2+ times just cancels out (2x = same as pressing 0x)
2. Order in which we press does not matter

Quick algo:
- Press each button once, then press 2 at a time, then 3, etc.
- For each combination, does pressing the button get us the target diagram?
- If so, record the # of buttons pressed into a master sum variable
- Return the master sum variable

"""
from itertools import combinations

def get_all_combinations(buttons):
    """Return list should already be sorted by length"""
    return [combo for i in range(1, len(buttons) + 1) for combo in list(combinations(buttons, i))]

def get_fewest_presses(target_light_diagram, combos):
    for combo in combos:
        current_light_diagram = [0] * len(target_light_diagram)
        for button in combo:
            for idx in button:
                current_light_diagram[idx] = 1 if current_light_diagram[idx] == 0 else 0

        if current_light_diagram == target_light_diagram:
            return len(combo)

# # Sample data
# data = "[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}"

sum_button_presses = 0

with open('day_10.txt', 'r') as file:
    for line in file:
        target_light_diagram, *buttons, joltage = line.strip().split()
        target_light_diagram = [0 if char == '.' else 1 for char in target_light_diagram[1:-1]]
        buttons = [tuple(map(int, button[1:-1].split(","))) for button in buttons]

        # Get all combinations
        combos = get_all_combinations(buttons)

        # For each combo (smallest # of buttons to largest), press each button and check if it matches the target diagram
        sum_button_presses += get_fewest_presses(target_light_diagram, combos)

print(sum_button_presses) # Part 1 complete
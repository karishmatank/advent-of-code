"""
Idea 1: Find a way to merge the entire set of rules into a 1D ordered list, where each number is in order.
We can then compare each update's numbers by taking a subset of the entire set and comparing the order for all numbers
in the update.

Idea 2: For each update, start with the first two numbers. If there is an entry in our rules with the first number at index 0
and the second at index 1, then move on to the second set of two numbers (indices 0 and 2). If at any point we don't find
the pair of numbers in the same order, the numbers are out of order
"""

rules = set() # More efficient for membership testing, which we will be using it for
updates = []

with open('day_5.txt', 'r') as file:
    for line in file:
        line = line.strip()
        if '|' in line:
            before, after = line.split('|')
            rules.add((before, after))
        elif line != '':
            pages = line.split(',')
            updates.append(pages)

# **************************************************************************************


def is_valid_update(update):
    for idx_start in range(0, len(update) - 1):
        for idx_end in range(idx_start + 1, len(update)):
            pair = (update[idx_start], update[idx_end])
            if pair not in rules:
                return False
    return True

def get_middle_page(update):
    middle_idx = len(update) // 2
    return update[middle_idx]

total_sum = 0
for update in updates:
    if is_valid_update(update):
        total_sum += int(get_middle_page(update))

print(total_sum) # Part 1 complete!






"""
How do we reorder an update?

97, 13, 75, 29, 47

Let's try bubble sort:
- 97 and 13 are ordered correctly as per the rules
- 13 and 75 are in the wrong order -> change to 97, 75, 13, 29, 47
- 13 and 29 are in the wrong order -> change to 97, 75, 29, 13, 47
- 13 and 47 are in the wrong order -> change to 97, 75, 29, 47, 13

- 97 and 75 in correct order, 75 and 29 in correct order, 29 and 47 in wrong order -> change to 97, 75, 47, 29, 13
- 29 and 13 in right order

- Going through once more, no more updates, so we are done
"""

def reorder_update(update):
    new_update = list(update)
    while True:
        num_changes = 0
        for idx in range(len(new_update) - 1):
            pair = (new_update[idx], new_update[idx+1])
            if pair not in rules:
                new_update[idx+1], new_update[idx] = new_update[idx], new_update[idx+1]
                num_changes += 1

        if num_changes == 0:
            break

    return new_update

total_sum = 0
for update in updates:
    reordered = reorder_update(update)
    if update != reordered:
        total_sum += int(get_middle_page(reordered))

print(total_sum) # Part 2 complete!
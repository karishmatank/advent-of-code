# Read in data, split by comma to get each range
with open("day_2.txt") as f:
    data = f.read()

data = data.split(",")

cumulative = 0

def is_invalid_part_1(num):
    # What constitutes an invalid number?
    # 1. The front half of the number matches the back half
    # 2. It's an even number of digits- 101 is not valid, but 1010 would be

    str_num = str(num)

    if len(str_num) % 2 != 0:
        return False

    half_idx = len(str_num) // 2
    return str_num[:half_idx] == str_num[half_idx:]

def is_invalid_part_2(num):
    # Similar to a problem where we figure out whether num can be decomposed into smaller parts t repeated k times
    # such that num = t * k
    # So t is a substring and k is a "factor"

    original = str(num)

    # I don't go to len + 1 here because I want to leave out the scenario where factor = 1
    # That means the ID is valid, so I don't want to return True
    for idx in range(1, len(original)):
        substr = original[:idx]

        # If we can't create a whole number factor, move on
        factor = len(original) / len(substr)
        if factor % 1 != 0:
            continue

        factor = int(factor)

        # Try to recreate original string out of substr and factor
        comp = substr * factor
        
        if comp == original:
            return True
    
    return False


# For each range, inclusive of start and finish, we want to find the invalid IDs
for rng in data:
    # First, we'll have to convert to ints
    start, end = [int(num) for num in rng.split("-")]
    
    # Create a range from start to end inclusive
    candidates = range(start, end + 1)

    # For each candidate, if invalid, add to a sum tracker variable
    # cumulative += sum(filter(is_invalid_part_1, candidates))
    cumulative += sum(filter(is_invalid_part_2, candidates))

print(cumulative) # Correct part 1 and 2
def cumulative_product(nums):
    product = 1
    for num in nums:
        product *= num
    return product

# Read in data
data = []

with open("day_6.txt", 'r') as file:
    for line in file:
        line = line.replace("\n", "")
        # line = line.split()
        data.append(line)

# All lines in the data are the same length
total_length = len(data[0])

groups = []
starting_idx = 0

for idx in range(total_length):
    # Look through each line within the given idx. If they are all spaces, then take whatever was to the left 
    all_spaces = all(line[idx] == " " for line in data)
    if all_spaces:
        nums = [line[starting_idx:idx] for line in data]
        groups.append(nums)
        starting_idx = idx + 1

# Append last group
nums = [line[starting_idx:] for line in data]
groups.append(nums)

grand_total = 0

for group in groups:
    *str_nums, operation = group
    operation = operation.strip()

    # We can now align each digit correctly with the vertical group it belongs to because we kept in all the spaces
    list_digits = [[digit for digit in num] for num in str_nums]
    correct_str_nums = zip(list_digits[0], list_digits[1], list_digits[2], list_digits[3])
    correct_nums = [int("".join(num)) for num in correct_str_nums]

    if operation == "+":
        total = sum(correct_nums)
    else:
        total = cumulative_product(correct_nums)

    grand_total += total

print(grand_total) # Part 2 correct
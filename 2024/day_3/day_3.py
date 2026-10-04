import re

with open('day_3.txt', 'r') as file:
    instructions = file.read()

valid_instructions = re.findall(r'mul\(\d{1,3},\d{1,3}\)', instructions)
numbers = [re.findall(r'\d+', instruction) for instruction in valid_instructions]

total_sum = 0
for num_set in numbers:
    num1, num2 = num_set
    total_sum += (int(num1) * int(num2))
print(total_sum) # Part 1 complete!




valid_instructions = re.findall(r"mul\(\d{1,3},\d{1,3}\)|do\(\)|don\'t\(\)", instructions)
total_sum = 0
enabled = True
for instruction in valid_instructions:
    # If the instruction has numbers, then parse them out
    numbers = re.findall(r'\d+', instruction)
    if numbers and enabled:
        num1, num2 = numbers
        total_sum += (int(num1) * int(num2))

    # If the instruction is a do instruction, then turn enabled to True
    elif instruction == 'do()':
        enabled = True

    # If the instruction is a don't instruction, turn enabled to False
    elif instruction == "don't()":
        enabled = False

print(total_sum) # Part 2 complete!
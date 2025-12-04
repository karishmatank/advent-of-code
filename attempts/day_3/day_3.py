"""
Part 2 notes:
bank = 789654321111111 (len = 15)

We need 12 batteries
For pass 1:
    - Remaining batteries = 12
    - We can only search [7896]54321111111 => If we searched 5 and to the right, we wouldn't have enough for 12
    - start_idx = 0
    - end_idx = 4 (exclusive) = len - remaining batteries + 1
    - We eventually should find 9 as the max digit

For pass 2:
    - Remaining batteries = 11
    - We should search beyond 9 now => bank becomes "654321111111" (len = 12)
    - We can only search [65]4321111111 => If we searched 4 and beyond, we wouldn't have enough for 11
    - start_idx = 0
    - end_idx = 2 (exclusive) = len - remaining batteries + 1
    - We eventually find 6 as the max digit

For pass 3:
    - Remaining batteries = 10
    - We search beyond 6 now => bank becomes "54321111111" (len = 11)
    - We can only search [54]321111111
    - start_idx = 0
    - end_idx = 2 (exclusive) = len - remaining batteries + 1

...
"""

# def get_largest_joltage(bank):
#     """Part 1 answer"""
#     # Step 1: Find first occurrence of largest digit (1-9) from indices 0 to len - 2
#     # Don't want to check last digit because there is no digit that comes after
#     for digit in range(9, 0, -1):
#         digit = str(digit)
#         start_digit_idx = bank.find(digit, 0, -1)
#         if start_digit_idx != -1:
#             break
    
#     first_digit = digit

#     # Step 2: Find largest digit that comes at a later index from step 1 result
#     second_digit = max(digit for digit in bank[start_digit_idx + 1:])

#     voltage = int(first_digit + second_digit)
#     return voltage

def get_largest_joltage(bank, num_batteries):
    """Part 2 answer, also works with part 1"""
    selected = []

    for num_batteries_needed in range(num_batteries, 0, -1):
        end_idx = len(bank) - num_batteries_needed + 1

        for digit in range(9, 0, -1):
            digit = str(digit)
            digit_idx = bank.find(digit, 0, end_idx)
            if digit_idx != -1:
                break
        
        selected.append(digit)

        bank = bank[digit_idx + 1:]
    
    voltage = int("".join(selected))
    return voltage
    

total_voltage = 0

with open("../../data/day_3.txt") as file:
    for line in file:
        line = line.replace("\n", "")
        total_voltage += get_largest_joltage(line, 12)

print(total_voltage)
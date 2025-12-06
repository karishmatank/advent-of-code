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
        line = line.split()
        data.append(line)

zipped = zip(data[0], data[1], data[2], data[3], data[4])

grand_total = 0

for group in zipped:
    *nums, operation = group
    nums = [int(num) for num in nums]

    if operation == "+":
        total = sum(nums)
    else:
        total = cumulative_product(nums)

    grand_total += total

print(grand_total) # Part 1 correct
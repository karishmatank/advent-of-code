from functools import reduce

class LocationList:
    def __init__(self):
        self._numbers = []
        self._summary = None

    def load(self, number):
        self._numbers.append(number)

    def sort(self):
        self._numbers.sort()

    def create_summary(self):
        """Create a summary of how many times each number occurs in the list"""
        def summarize(acc, next):
            acc.setdefault(next, 0)
            acc[next] += 1
            return acc
        self._summary = reduce(summarize, self._numbers, {})

    def __len__(self):
        return len(self._numbers)

    def __getitem__(self, idx):
        return self._numbers[idx]

    def get_num_occurrences(self, num):
        """Get the number of times the input occurs within the list"""
        return self._summary.get(num, 0)

    def __iter__(self):
        for number in self._numbers:
            yield number


# Create both lists
left_list = LocationList()
right_list = LocationList()

# Parse the data to get each list
with open('day_1.txt', 'r') as file:
    for line in file:
        left, right = line.split()
        left_list.load(int(left))
        right_list.load(int(right))

# Sort the lists from smallest to largest
left_list.sort()
right_list.sort()

# Both lists contain 1000 numbers
# print(len(left_list))
# print(len(right_list))

# For each list, get the smallest from each, find the abs value of the distance, store it
distance = 0

for idx in range(0, len(left_list)):
    distance += abs(left_list[idx] - right_list[idx])

print(distance) # Part 1 complete!



# Create the summary for the right list
right_list.create_summary()

# For each number in the left list, find how many times it occurs in the right list
# Compute similarity score (number * occurrences)
# Keep track of total sum
total_sum = 0
for number in left_list:
    occurrences = right_list.get_num_occurrences(number)
    total_sum += (number * occurrences)
print(total_sum) # Part 2 complete!
# Get data

# Ranges represent fresh ingredients, following list represents available ingredients
fresh_id_ranges = []
candidate_ids = []

min_id = None
max_id = None

with open('day_5.txt', 'r') as file:
    for line in file:
        line = line.replace("\n", "")

        # Record all IDs that represent fresh ingredients
        if "-" in line:
            start, end = [int(num) for num in line.split("-")]
            fresh_id_ranges.append(range(start, end + 1)) # The ranges we get are inclusive of start and end

            if min_id is None or start < min_id:
                min_id = start

            if max_id is None or end > max_id:
                max_id = end
        
        # Skip over the empty line
        elif line == "":
            continue

        # These will all come after all the ranges are populated from the if block
        # We will check each number to see if it is present in the set
        else:
            candidate_ids.append(int(line))

fresh_counter = 0

# Check candidate IDs in each range
for i in candidate_ids:
    for rng in fresh_id_ranges:
        if i in rng:
            fresh_counter += 1
            break

print(fresh_counter) # Part 1 complete



# How many total ingredient IDs are considered to be fresh according to the ranges?
# Can't use a set to find each unique ID, as that takes too much memory

# First, we'll sort the ranges based on start
sorted_ranges = sorted(fresh_id_ranges, key=lambda rng: rng.start)

# Then, we'll check the ranges in order to see if there is overlap
# Combine ranges if there is overlap

def is_overlap(rng_earlier_start, rng2_later_start):
    return rng2_later_start.start < rng_earlier_start.stop

def combine_ranges(rng_earlier_start, rng2_later_start):
    max_end = max(rng_earlier_start.stop, rng2_later_start.stop)
    return range(rng_earlier_start.start, max_end)

# Check overlap based on latest range in combined_ranges
combined_ranges = [sorted_ranges[0]]

for rng in sorted_ranges[1:]:
    if is_overlap(combined_ranges[-1], rng):
        new_rng = combine_ranges(combined_ranges[-1], rng)
        combined_ranges.pop()
        combined_ranges.append(new_rng)
    else:
        combined_ranges.append(rng)

# Sum the number of IDs within each range
num_ids = sum(len(rng) for rng in combined_ranges)

print(num_ids) # Part 2 complete
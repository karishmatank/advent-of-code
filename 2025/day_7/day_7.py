# Read in data
with open('day_7.txt', 'r') as file:
    data = file.readlines()

beam_idxs = set()
num_splits = 0

for line in data:
    for current_idx in range(len(line)):
        if line[current_idx] == 'S':
            beam_idxs.add(current_idx)
        
        # Split occurs if we run into ^ and beam exists in same position of line above
        if line[current_idx] == '^' and current_idx in beam_idxs:
            # Record split
            num_splits += 1

            # Record change in where the beam now is
            beam_idxs.discard(current_idx)
            beam_idxs.update([current_idx-1, current_idx+1])

print(num_splits) # Part 1 complete
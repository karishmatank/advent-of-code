"""
Trying part 2 again by first finding all paths to dac, then to fft, then to out. 
We can then try to multiply those 3 to find the total # of paths that go through dac and fft
Saw this hint on reddit

Also saw hint on reddit to use lru_cache, what a timesaver, so quick
- This is possible with this implementation because lru_cache will cache the calls to traverse_function with the same input
- We've now simplified the input to include one argument, vs the history that I was trying to attach alongside it
- It didn't cache before because that history would always be different based on different paths leading up to the node
"""

from functools import lru_cache

# Read data into a dictionary

connections = dict()

with open('day_11.txt', 'r') as file:
    for line in file:
        device, *to = line.strip().split()
        device = device.strip(":")
        connections[device] = to

# # Test data
# connections = {
#     "svr": ["aaa", "bbb"],
#     "aaa": ["fft"],
#     "fft": ["ccc"],
#     "bbb": ["tty"],
#     "tty": ["ccc"],
#     "ccc": ["ddd", "eee"],
#     "ddd": ["hub"],
#     "hub": ["fff"],
#     "eee": ["dac"],
#     "dac": ["fff"],
#     "fff": ["ggg", "hhh"],
#     "ggg": ["out"],
#     "hhh": ["out"]
# }

# start_pos = 'svr'
# end_pos = "dac"
# mandatory_devices = ['dac', 'fft']

# Recursively look through paths to find all that go from start_pos to end_pos
# This time, we need to keep track of the path itself too, to check whether 'dac' or 'fft' are in it

@lru_cache(maxsize=None)
def traverse_connections(start, end):
    # Check if end_pos symbol is in the connections list for start symbol
    # If so, return 1
    # If not, check from the resulting new start positions

    path_counter = 0

    if end in connections[start]:
        return 1
        
    # # Check to make sure there aren't any cycles
    # if start in history:
    #     return 0
    
    # # Update the current branch's path
    # new_history = list(history)
    # new_history.append(start)

    for next_conn in connections[start]:
        # If we reach out but we weren't looking for out (end != 'out'), then we've reached a dead end
        if next_conn != 'out':
            path_counter += traverse_connections(next_conn, end)

    return path_counter

# Two ways we can get from 'svr' to 'out' while running through 'fft' and 'dac'
# 1. 'svr' -> 'fft' -> 'dac' -> 'out'
# 2. 'svr' -> 'dac' -> 'fft' -> 'out'

total = 0

for path in [['svr', 'fft', 'dac', 'out'], ['svr', 'dac', 'fft', 'out']]:
    num_connections = 1
    
    for idx in range(len(path) - 1):
        num_connections *= traverse_connections(path[idx], path[idx + 1])
    
    total += num_connections

print(total) # Part 2 complete!!!
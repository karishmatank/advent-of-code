"""
Notes:
Part 2 incomplete, too slow in its current form.
Works great with the simple test data.
Function traverse_connections is doing too much re also maintaining history, would have to reorganize that
Probably a better way to keep track of cycles without the entire history?
"""


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

start_pos = 'svr'
end_pos = "out"
mandatory_devices = ['dac', 'fft']

# Recursively look through paths to find all that go from start_pos to end_pos
# This time, we need to keep track of the path itself too, to check whether 'dac' or 'fft' are in it

def traverse_connections(start, history):
    # Check if end_pos symbol is in the connections list for start symbol
    # If so, return 1
    # If not, check from the resulting new start positions

    path_counter = 0

    if end_pos in connections[start]:
        # Check if each of the mandatory devices is in our history
        if all(device in history for device in mandatory_devices):
            return 1
        else:
            return 0
        
    # Check to make sure there aren't any cycles
    if start in history:
        return 0
    
    # Update the current branch's path
    new_history = list(history)
    new_history.append(start)

    for next_conn in connections[start]:
        path_counter += traverse_connections(next_conn, new_history)

    return path_counter

print(traverse_connections(start_pos, []))
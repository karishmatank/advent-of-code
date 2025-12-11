# Read data into a dictionary

connections = dict()

with open('day_11.txt', 'r') as file:
    for line in file:
        device, *to = line.strip().split()
        device = device.strip(":")
        connections[device] = to

# Test data
# connections = {
#     "aaa": ["you", "hhh"],
#     "you": ["bbb", "ccc"],
#     "bbb": ["ddd", "eee"],
#     "ccc": ["ddd", "eee", "fff"],
#     "ddd": ["ggg"],
#     "eee": ["out"],
#     "fff": ["out"],
#     "ggg": ["out"],
#     "hhh": ["ccc", "fff", "iii"],
#     "iii": ["out"]
# }

start_pos = 'you'
end_pos = "out"

# Recursively look through paths to find all that go from start_pos to end_pos
def traverse_connections(start):
    # Check if end_pos symbol is in the connections list for start symbol
    # If so, return 1
    # If not, check from the resulting new start positions

    path_counter = 0

    if end_pos in connections[start]:
        return 1
    
    for next_conn in connections[start]:
        path_counter += traverse_connections(next_conn)

    return path_counter

print(traverse_connections(start_pos)) # Part 1 complete
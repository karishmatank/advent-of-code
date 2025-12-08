import math

# data = [
#     (162,817,812),
#     (57,618,57),
#     (906,360,560),
#     (592,479,940),
#     (352,342,300),
#     (466,668,158),
#     (542,29,236),
#     (431,825,988),
#     (739,650,466),
#     (52,470,668),
#     (216,146,977),
#     (819,987,18),
#     (117,168,530),
#     (805,96,715),
#     (346,949,466),
#     (970,615,88),
#     (941,993,340),
#     (862,61,35),
#     (984,92,344),
#     (425,690,689)
# ]

# Read in data

with open('day_8.txt', 'r') as file:
    data = file.readlines()

data = [line.replace("\n", "").split(',') for line in data]
data = [[int(num) for num in lst] for lst in data]
data = [tuple(lst) for lst in data]


def euclidian_distance(pos1, pos2):
    # Match the x's together, y's, z's
    matched = list(zip(pos1, pos2))

    total_sum = 0
    for pair in matched:
        # Subtract nums and take square
        total_sum += (pair[0] - pair[1]) ** 2
    return math.sqrt(total_sum)

def get_shortest_connections(num_connections):
    pair_dist = {}

    for idx in range(len(data)):
        for idx2 in range(idx + 1, len(data)):
            pair = (data[idx], data[idx2])
            distance = euclidian_distance(*pair)
            pair_dist[pair] = distance

    sorted_connections = sorted(list(pair_dist.keys()), key=lambda pair: pair_dist[pair])
    return sorted_connections[:num_connections]

def calc_product(nums):
    prod = 1
    for num in nums:
        prod *= num
    return prod

# Given the shortest connections, create circuits
# We'll represent a circuit by the unique boxes that make up that circuit
connections = get_shortest_connections(1000)

circuits = []
for connection in connections:
    # print(f"current connection={connection}")

    circuits_to_remove = []
    new_circuits = []

    # If any one of the boxes in the connection is in a circuit, add all boxes in the connection to that circuit
    for circuit in circuits:
        # print(f"current circuit={circuit}")
        if any(box in circuit for box in connection):
            # print(f"a box is in the circuit!")

            # I take the approach here of noting that we want to later remove the circuit in its current form
            # from the list of circuits, while retaining that info to create a new circuit that we will
            # later append to our list of circuits
            circuits_to_remove.append(circuit)
            new_circuit = set(circuit)
            new_circuit.update(connection)
            # print(f"new circuit = {new_circuit}")

            # I keep a separate list of new circuits as we will be able to connect them after the latest changes
            # We can connect them because we are iterating through circuits over the same connection
            # which means that if the same connection has boxes present in multiple circuits, they should be connected
            # into one master circuit
            new_circuits.append(new_circuit)

    # Merge together the new circuits and add to circuits list
    if new_circuits:
        circuit_to_append = set()
        for new_cir in new_circuits:
            circuit_to_append.update(new_cir)
        circuits.append(circuit_to_append)
    
    # Else, create a new circuit
    else:
        # print(f"No boxes in any circuit, new circuit created!")
        new_conn = set(connection)
        circuits.append(new_conn)

    # Remove each of the circuits we're supposed to remove
    for cir in circuits_to_remove:
        circuits.remove(cir)        

    # print()

# Sort lengths of largest circuits. Add in lengths of 1 to represent boxes that are not connected
largest_lens = [len(circuit) for circuit in circuits]
largest_lens.extend(1 for _ in range(len(data) - sum(largest_lens)))
sorted_lens = sorted(largest_lens, reverse=True)

# Get product of 3 largest circuit lengths
print(calc_product(sorted_lens[:3])) # Part 1 correct
"""
.......S....... [.......1.......]
.......|....... [.......1.......]
......|^....... [......101......] (can't reach position under splitter anymore since it split)
......|........ [......101......] => sum is 2

For the mini example above, there are 2 possible timelines, either it splits left or right.

.......S....... [.......1.......]
.......|....... [.......1.......]
......|^....... [......101......]
......|........ [......101......]
.....|^.^...... [.....10201.....] (can't reach under splitter, can reach around it, increment those vals by 1)
.....|......... [.....10201.....] => sum is 4

For this expanded example, there are 4 possible timelines, either it goes LL, LR, RL, or RR

.......S....... [.......1.......]
.......|....... [.......1.......]
......|^....... [......101......]
......|........ [......101......]
.....|^.^...... [.....10201.....]
.....|......... [.....10201.....]
....|^.^.^..... [....1030301....] (set value of idx of splitter to 0, but take num of row above it...
....|.......... [....1030301....] (...and add that to idxs to left and right of splitter) => sum is 8

Now, there are 8 possible timelines, LLL, LLR, LRL, LRR, RLL, RLR, RRL, RRR

.......S.......
.......|.......
......|^.......
......|........
.....|^.^......
.....|.........
....|^.^.^..... [....1030301....]
....|.......... [....1030301....]
...|^.^...^.... [...104033101...] (num of row above splitter represents # of paths that a beam can get to splitter)
...|........... [...104033101...] => sum is 13

LLLL, LLLR, LLRL, LLRR, LRLL, LRLR, LRR, RLLL, RLLR, RLR, RRL, RRRL, RRRR => 13
"""

# Read in data
with open('day_7.txt', 'r') as file:
    data = file.readlines()

data = [line.replace("\n", "") for line in data]

# data = [
#     ".......S.......",
#     ".......|.......",
#     "......|^.......",
#     "......|........",
#     ".....|^.^......",
#     ".....|.........",
#     "....|^.^.^.....",
#     "....|..........",
#     "....^|^...^....",
#     ".....|.........",
#     "...^.^|..^.^...",
#     "......|........",
#     "..^..|^.....^..",
#     ".....|.........",
#     ".^.^.^|^.^...^.",
#     "......|........"
# ]


prior_row_path_counts = None

for line in data:
    row_path_count = prior_row_path_counts if prior_row_path_counts else [0] * len(line)
    
    for current_idx in range(len(line)):
        if line[current_idx] == 'S':
            # One way to get to the position where 'S' is- only related to first row
            row_path_count[current_idx] = 1
        
        # Split occurs if we run into ^ and beam exists in same position of line above
        elif line[current_idx] == '^':
            # In this case, as per examples above, we take the number of paths that exist where beam could reach ^
            # and then we add that number to the indices to the left and right of the current index, on the current row
            # We then set the number of paths for the ^ index to 0, as no beams can go through the splitter
            paths_reaching_splitter = prior_row_path_counts[current_idx]
            row_path_count[current_idx - 1] += paths_reaching_splitter
            row_path_count[current_idx + 1] += paths_reaching_splitter
            row_path_count[current_idx] = 0
    
    prior_row_path_counts = row_path_count

print(sum(prior_row_path_counts)) # Part 2 complete!

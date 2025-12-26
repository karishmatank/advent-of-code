"""
Quick algo for getting fewest presses:
- For each combo
    - Represent each button as a list i.e. (3) => [0, 0, 0, 1] or (1, 3) => [0, 1, 0, 1]
    - Have to try to do some sort of linear combo exercise to figure out what freq of buttons gets us the joltage
    - Record the total # of presses required (sum of presses per button) for each combo
- Across combos, record the min # as you go
- Return that min number

Issue is that it seems we can't solve this using linear algebra, as we need A to be square to use the numpy functionality.
    - A = each button is a column
    - x = solve for this
    - b = joltage (4x1)
A likely won't be square, as we have combos that have different #s of buttons, so joltage length not necessarily = to
# of buttons.

I came back to try to use np.linalg.pinv to solve for the least squares solution, which theoretically works for non-square As
but it's not guaranteed to converge + rounding up/down the solution isn't guaranteed to be correct. 
It worked for the test cases but not for the input.

I then came back to try to use Gaussian elimination to actually solve. I've implemented a few steps so far:
    - Check if it is worth trying for Gaussian elimination, or perhaps the combination selected would never work anyway
    - If so, 1) make sure row has a pivot, if not, swap rows until it does, 2) eliminate rows below such that col has 0s
      in rows below the pivot
    - Account for when we have more columns than rows. In that case, the last X columns represent free variables
    - When we have free variables, calculate solution by finding constraints on free variables and calculating mininum
      number of total presses. This last part is still a work in progress- it works for the tests but not for all
      of the lines of actual data. I think there's an issue with how I'm handling multiple free variables that I'll
      come back to.

So I'll leave it here for part 2 then...

"""
from itertools import combinations
import numpy as np


def get_all_combinations(buttons):
    """Return list should already be sorted by length"""
    return [combo for i in range(1, len(buttons) + 1) for combo in list(combinations(buttons, i))]

def button_to_list(button, total_elements):
    lst = [0] * total_elements
    for idx in button:
        lst[idx] = 1
    return lst

def is_valid_matrix(augmented_mat):
    # If there are any rows in A that are all 0 but b is non zero, a solution is impossible, don't even try
    # Similarly, if any of the last column (b col) are decimals, matrix is invalid
    for row in augmented_mat:
        *A, b = row   
        if all(num == 0 for num in A) and b != 0:
            return False
        if b % 1 != 0:
            return False
    return True

def position_rows(matrix, idx_row, idx_col):
    # Swap rows if we don't have a pivot (if A[idx_col][idx_col] is 0)
    num_rows = len(matrix)

    # Pivot exists if A[idx_row][idx_col] should be populated (!= 0)
    # If it isn't, need to swap rows. Find first row > idx_col where A[idx_row][idx_col] != 0
    if matrix[idx_row][idx_col] == 0:
        for idx_row_future in range(idx_row + 1, num_rows):
            if matrix[idx_row_future][idx_col] != 0:
                current_row = matrix[idx_row_future].copy()
                matrix[idx_row_future] = matrix[idx_row]
                matrix[idx_row] = current_row
                break    

def is_pivot(matrix, idx_row, idx_col):
    # Check to make sure there is actually a pivot where we think there should be
    # This returns True if the prior position_rows call is True, else False
    return matrix[idx_row][idx_col] != 0

def scale_row(matrix, idx_row, idx_col):
    # If pivot is negative, need to scale it / multiply it to be 1
    # If pivot is positive but greater than 1, need to scale it to be 1
    # Otherwise, pivot is 1 so we are fine

    factor = matrix[idx_row][idx_col]
    matrix[idx_row] = matrix[idx_row] / factor


def eliminate_below(matrix, idx_row, idx_col):
    num_rows = len(matrix)

    # For each row and given idx_col, reduce rows below such that matrix is 0
    for idx_row_future in range(idx_row + 1, num_rows):
        num = matrix[idx_row_future][idx_col]

        # Entry is not 0 already. If so, scale current row and add at idx_col index to row at idx_row index
        if num != 0:
            factor = -num
            matrix[idx_row_future] = [matrix[idx_row_future][idx] + (matrix[idx_row][idx] * factor) for idx in range(len(matrix[idx_row_future]))]

def eliminate_above(matrix, idx_row, idx_col):
    for idx_row_prior in range(idx_row):
        num = matrix[idx_row_prior][idx_col]

        # Entry is not 0 already. If so, scale current row and add to each prior rows
        if num != 0:
            factor = -num
            matrix[idx_row_prior] = [matrix[idx_row_prior][idx] + (matrix[idx_row][idx] * factor) for idx in range(len(matrix[idx_row_prior]))]

def gaussian_elimination(A, b):
    augmented_mat = np.column_stack((A, b)).astype(float)
    # print(f"Original augmented mat:\n {augmented_mat}")

    if not is_valid_matrix(augmented_mat):
        return None

    # For each column, 
    # 1) make sure there is a pivot in the correct row, 
    # 2) scale the pivot row so the pivot = 1
    # 3) eliminate numbers in the rows below the pivot within the same column
    num_rows = len(A)
    num_cols = len(A[0])

    current_row = 0

    for idx_col in range(num_cols):
        # If our current row exceeds the number of rows we have, then we should just stop
        if current_row >= num_rows:
            break
        
        # Position rows such that there is a pivot in the correct row
        position_rows(augmented_mat, current_row, idx_col)

        # Check to make sure there is a pivot in the column. If not, move to the next column
        # This keeps the current_row at the same value, as we want to check from the same row in the next column
        if not is_pivot(augmented_mat, current_row, idx_col):
            continue
        
        # print(f"New augmented mat after row positioning for idx_col {idx_col}:\n {augmented_mat}")

        # We'll scale the row by multiplying by -1 if the pivot is -1 for some reason.
        # Otherwise, pivot is 1 and we can move on
        scale_row(augmented_mat, current_row, idx_col)

        # print("After scaling:")
        # print(augmented_mat)

        # Eliminate below to achieve row echelon form
        eliminate_below(augmented_mat, current_row, idx_col)
        # print(f"New augmented mat after eliminating below for idx_col {idx_col}:\n {augmented_mat}")

        # Eliminate above to achieve reduced row echelon form
        eliminate_above(augmented_mat, current_row, idx_col)
        # print(f"New augmented mat after eliminating above for idx_col {idx_col}:\n {augmented_mat}")

        # Increment row tracker
        current_row += 1

    # Lastly, check to make sure matrix is valid to try to solve
    # print(f"Final augmented mat: {augmented_mat}")

    if not is_valid_matrix(augmented_mat):
        # print("Not valid!!!")
        return None
    
    return augmented_mat

def get_free_variables(augmented_mat):
    num_vars = len(augmented_mat[0]) - 1
    num_rows = len(augmented_mat)

    pivot_vars = set()

    for idx_row in range(num_rows):
        for idx_col in range(num_vars):
            if augmented_mat[idx_row][idx_col] == 1:
                pivot_vars.add(idx_col)
                break

    free_vars = [idx_col for idx_col in range(num_vars) if idx_col not in pivot_vars]
    return free_vars


# def extract_simple_solution(augmented_mat):
#     solutions = [int(row[-1]) for row in augmented_mat]
    
#     # Check that solution doesn't have weird negative values
#     if not all(num >= 0 for num in solutions):
#         return None
    
#     return sum(solutions)

def extract_simple_solution(augmented_mat):
    print("\n--- SIMPLE SOLUTION DEBUG ---")
    print("RREF matrix:")
    print(augmented_mat)
    
    last_col = [row[-1] for row in augmented_mat]  # Keep as float!
    print(f"Last column (as floats): {last_col}")
    print(f"All >= 0? {all(num >= -1e-10 for num in last_col)}")
    print(f"Close to integers? {[abs(num - round(num)) for num in last_col]}")
    
    # Check negative with tolerance
    if not all(num >= -1e-10 for num in last_col):
        print("REJECTED: Negative values")
        return None
    
    # Check integer with tolerance
    if not all(abs(num - round(num)) < 1e-6 for num in last_col):
        print("REJECTED: Not integers")
        return None
    
    result = sum(round(num) for num in last_col)
    print(f"ACCEPTED: sum = {result}")
    return result

def extract_complicated_solution(augmented_mat, free_variables):
    print("\n--- COMPLICATED SOLUTION DEBUG ---")
    print("Number of free vars:", len(free_variables))

    # For each variable, figure out whether to maximize or minimize
    # Example:
    # [[1 0 0 1 0 2]
    #  [0 1 0 0 0 5]
    #  [0 0 1 1 0 1]
    #  [0 0 0 0 1 3]]
    # x0 + x3 = 2 => x0 = 2 - x3 => Since x0 can't be negative, x3 would be 0 to 2 inclusive
    # x1 = 5
    # x2 + x3 = 1 => x2 = 1 - x3 => Since x2 can't be negative, x3 would be 0 to 1 inclusive
    # x4 = 3
    # 
    # x3 between 0 and 1 inclusive is more restrictive, so x3 can only be 0 or 1. 

    # If we add up all the expressions above (x0 + x1 + x2 + x3 + x4), we get the number of total button presses
    # We want to minimize that. If we simplify the sum in this example, we'll get that we should minimize 11 - x3.
    # Because x3 has a negative coefficient, we need to maximize x3 to minimize the sum.
    # Because we need to maximize x3 and its range is [0, 1], x3 is 1.
    # Therefore, x0 = 1, x1 = 5, x2 = 0, x3 = 1, x4 = 3 => total sum of presses is 10

    # Find the free variable's constraints first based on the formulas where its coefficient is positive in the matrix.
    #   - Don't use formulas where coeff is negative in matrix -> that translates to rewriting in terms of the pivot
    #     variable with the free var's coefficient as positive, which doesn't help us find the min number of times we
    #     can press the free var
    # If the sum of coeff of free variable col + 1 is +, we need to minimize the free var
    # If the sum of coeff of free variable col + 1 is -, we need to maximize the free var


    # Build a mapping for which row controls which variable (column)
    num_vars = len(augmented_mat[0]) - 1

    var_to_row = {}
    for row_idx, row in enumerate(augmented_mat):
        for col_idx in range(num_vars):
            if abs(row[col_idx] - 1.0) < 1e-10:  # Found pivot
                var_to_row[col_idx] = row_idx
                break

    free_var_values = []

    # For each free variable, compute its coefficient in the sum
    for free_var in free_variables:
        # Coefficient starts at 1, since the sum of x0 + x1 + ... + xn will include an entry for the free variable itself
        sum_coeff = 1

        # Subtract coefficients from pivot variable rows
        # In the example above, this is akin to x0 + x3 = 2 => x0 = 2 - x3 (sign of x3 flips)
        for pivot_var, row_idx in var_to_row.items():
            sum_coeff -= augmented_mat[row_idx][free_var]
        
        # Find constraints- each variable >= 0, for each pivot: constant - coeff * free_var >= 0
        max_free_val = float('inf')
        min_free_val = 0

        for pivot_var, row_idx in var_to_row.items():
            coeff = augmented_mat[row_idx][free_var]
            constant = augmented_mat[row_idx][-1]
            if coeff > 0:  # constraint: constant - coeff*free_var >= 0
                max_free_val = min(max_free_val, constant / coeff)
            elif coeff < 0:
                min_free_val = max(min_free_val, constant / coeff)

        # Optimize: if coefficient negative, maximize; if positive, minimize
        if sum_coeff < 0:
            free_var_value = max_free_val if max_free_val != float('inf') else min_free_val
        else:
            free_var_value = min_free_val

        free_var_values.append(free_var_value)

    # Compute actual variable values
    # If free variable, get it from the values we just calculated
    # Otherwise, need to calculate variable value based on value of free var
    # Ex: x0 = 2 - x3 => x3 is free variable, get its value, subtract from b of that row
    result = []
    for var_idx in range(num_vars):
        if var_idx in free_variables:
            free_var_value = free_var_values[free_variables.index(var_idx)]
            result.append(free_var_value)
        else:
            row_idx = var_to_row[var_idx]
            value = augmented_mat[row_idx][-1]
            for fv in free_variables:
                free_var_value = free_var_values[free_variables.index(fv)]
                value -= augmented_mat[row_idx][fv] * free_var_value
            result.append(value)


    # Check that last col doesn't have weird negative values
    if not all(num >= 0 for num in result):
        return None

    # Check that values are close to integers
    if any(abs(num - round(num)) > 1e-6 for num in result):
        return None

    return sum(round(v) for v in result) # Safe to round


def get_fewest_presses(target_joltage, combos):
    min_presses = None
    total_combos = len(combos)
    valid_solutions = 0
    invalid_rref = 0
    invalid_solution = 0

    for combo in combos:        
        # Represent each button in the combo as a list
        buttons = [button_to_list(button, len(target_joltage)) for button in combo]
        
        # Solve system of equations
        A = np.array(buttons).T
        b = np.array([[i] for i in target_joltage])
        # print(A)
        # print(b)

        # 1. To solve system of equations, we first get its RREF form
        rref = gaussian_elimination(A, b)
        if rref is None:
            invalid_rref += 1
            continue
        
        # print(f"{rref=}")

        # 2. Next, we find the free variables (cols without pivot rows)
        free_vars = get_free_variables(rref)

        # print(f"{free_vars=}")

        # 3. Find solution
        if len(free_vars) == 0:
            # print(free_vars)
            solution = extract_simple_solution(rref)
        else:
            solution = extract_complicated_solution(rref, free_vars)

        # print(f"{solution=}")
        if solution is None:
            invalid_solution += 1


            print("\n" + "="*60)
            print("DEBUGGING REJECTED SOLUTION")
            print("="*60)

            print("\n1. ORIGINAL SYSTEM:")
            print("Buttons in combo:", combo)
            print("A matrix:")
            print(A)
            print("b vector:", b.T)

            print("\n2. RREF:")
            print(rref)

            print("\n3. FREE VARIABLES:")
            print(free_vars)

            # print("\n4. EXTRACTED SOLUTION:")
            # print("Solution values:", result)  # or whatever you computed
            # print("Rejection reason: [negative/non-integer/etc]")

            # print("\n5. MANUAL VERIFICATION:")
            # # Simulate what happens if we use this solution
            # simulated = [0] * len(joltage)
            # for button_idx, presses in enumerate(result):
            #     button = debug_combo[button_idx]
            #     for counter in button:
            #         simulated[counter] += presses
            # print("Target joltage:", list(b.flatten()))
            # print("Simulated result:", simulated)
            # print("Match?", simulated == list(b.flatten()))









            continue

        # 4. Update minimum
        valid_solutions += 1
        if not min_presses or solution < min_presses:
            min_presses = solution
            print(f"New minimum: {min_presses} from combo {combo}")

    print(f"\nStats:")
    print(f"Total combos: {total_combos}")
    print(f"Invalid RREF: {invalid_rref}")
    print(f"Invalid solutions: {invalid_solution}")
    print(f"Valid solutions: {valid_solutions}")
    
    # print(combo)
    # print(min_presses)
    return min_presses




# Sample data
# line = "[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}"
# line = "[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}"
# line = "[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"
# line = "[##...#] (1,3,4,5) (2,3,5) (0,2,3) (0,2,3,4,5) (1,2,4) (0,1,2,3) {24,27,40,30,25,17}"
line = "[...####.#.] (0,1,4,5,8) (4,6,7) (1,3,4,5,6,8,9) (0,5,9) (1,2,4,5,9) (0,2,3,4,5,6,7,8) (0,5,6,9) (1,3,8,9) (1,3,5,7,8,9) (4,5,7) (1,3,5,6,7,8,9) (1,2,4,5,6,7,8) (3,5,6,7) {145,40,16,28,49,200,23,46,32,152}"

# For each of the above, answers are 10, 12, 11

sum_button_presses = 0

# with open('day_10.txt', 'r') as file:
#     for line in file:
target_light_diagram, *buttons, joltage = line.strip().split()
buttons = [tuple(map(int, button[1:-1].split(","))) for button in buttons]
joltage = [int(num) for num in joltage[1:-1].split(",")]

# print(line)

# Get all combinations
combos = get_all_combinations(buttons)
sum_button_presses += get_fewest_presses(joltage, combos)

print(sum_button_presses) # Works with the test cases, but for at least one of the input lines, doesn't converge for any combo
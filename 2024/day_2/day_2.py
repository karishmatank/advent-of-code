def is_increasing(report):
    return sorted(report) == report

def is_decreasing(report):
    return sorted(report, reverse=True) == report

def has_valid_jumps(report):
    for idx in range(1, len(report)):
        jump = abs(report[idx] - report[idx-1])
        if jump < 1 or jump > 3:
            return False
    return True

def is_valid_report(report):
    return (is_increasing(report) or is_decreasing(report)) and has_valid_jumps(report)

def create_report_variations(report):
    """Return all unique variations of the report with 0 or 1 removed element"""
    variations = [report]
    for idx in range(0, len(report)):
        # Shallow copy is fine, numbers are immutable
        new_report = list(report)
        new_report.pop(idx)
        variations.append(new_report)
    return variations



# **************************************************************************************

# Read in all reports, where each report is a list whose elements are its levels
with open('day_2.txt', 'r') as file:
    reports = file.readlines()
reports = [[int(num) for num in report.strip().split()] for report in reports]

# For each report, determine whether it is safe
# Strictly increasing, strictly decreasing, each "jump" between levels is 1, 2, or 3
total_valid = 0
for report in reports:
    if is_valid_report(report):
        total_valid += 1

print(total_valid) # Part 1 complete!



total_valid = 0
for report in reports:
    variations = create_report_variations(report)
    for variation in variations:
        if is_valid_report(variation):
            total_valid += 1
            break
print(total_valid) # Part 2 complete!
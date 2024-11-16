
# Subject group data and student counts
subject_groups =  {
('ML', 'IS', 'CC', 'DF'):138,
('ML', 'IS', 'CC', 'MAD'):6,
('ML', 'IS', 'MCWC', 'MAD'):2,
('ML', 'IS', 'MCWC', 'DF'):3,
('BDA', 'IS', 'MCWC', 'MAD'):9,
('BDA', 'IS', 'CC', 'DF'):9,
('BDA', 'IS', 'CC', 'MAD'):1,
('BDA', 'IS', 'MCWC', 'DF'):10,
}

# Initial subject hours
total_hours = {
    "ML": 5,
    "BDA": 5,
    "IS": 5,
    "MCWC": 3,
    "CC": 3,
    "MAD": 4,
    "DF": 4
}

# Constraints
min_students = 0  # No minimum size for divisions
max_students = 90  # Maximum size per division

def allocate_groups_with_splitting(subject_groups, total_hours, min_students, max_students):
    # Step 1: Preprocess subject groups to split any group exceeding max_students
    preprocessed_groups = []
    for group, count in subject_groups.items():
        while count > max_students:            
            preprocessed_groups.append((group, max_students))
            count -= max_students
        if count > 0:
            preprocessed_groups.append((group, count))        
    # Step 2: Initialize variables for the backtracking algorithm
    groups = [group for group, _ in preprocessed_groups]
    students = [count for _, count in preprocessed_groups]    
    best_solution = {"divisions": None, "deviation": float("inf")}
    recursive_calls = 0

    def calculate_hours(division):
        """Calculate total hours per subject in a division."""
        hours = {subject: 0 for subject in total_hours}
        for group, _ in division:
            for subject in group:
                hours[subject] = total_hours[subject]
        return hours

    def calculate_deviation(hours):
        """Calculate the total deviation of hours from the initial requirement."""
        return sum(abs(hours[sub] - total_hours[sub]) for sub in total_hours)

    def backtrack(current_divisions, remaining_groups, remaining_counts):
        nonlocal recursive_calls
        recursive_calls += 1

        # Base case: no groups left to allocate
        if not remaining_groups:
            print('here')
            total_hours_all = {subject: 0 for subject in total_hours}
            for division in current_divisions:
                hours = calculate_hours(division)
                for subject in total_hours_all:
                    total_hours_all[subject] += hours[subject]
            deviation = calculate_deviation(total_hours_all)
            if deviation < best_solution["deviation"]:
                best_solution["divisions"] = [div[:] for div in current_divisions]
                best_solution["deviation"] = deviation
            return

        # Get the next group and its student count
        group = remaining_groups[0]
        count = remaining_counts[0]

        # Try allocating the group (or part of it) to each division
        for i in range(len(current_divisions)):
            division = current_divisions[i]
            division_student_count = sum(student_count for _, student_count in division)

            if division_student_count + count <= max_students:
                # Allocate the entire group to this division
                division.append((group, count))
                backtrack(
                    current_divisions,
                    remaining_groups[1:],
                    remaining_counts[1:],
                )
                # Backtrack
                division.pop()
            else:
                # Allocate a part of the group to this division
                split_count = max_students - division_student_count
                if split_count > 0:
                    # Add the split part to this division
                    division.append((group, split_count))
                    # Recurse with the remaining students of the group
                    backtrack(
                        current_divisions,
                        [group] + remaining_groups[1:],
                        [count - split_count] + remaining_counts[1:],
                    )
                    # Backtrack
                    division.pop()

        # Start a new division with this group
        if len(current_divisions) < len(groups):
            current_divisions.append([(group, count)])
            backtrack(
                current_divisions,
                remaining_groups[1:],
                remaining_counts[1:],
            )
            # Backtrack
            current_divisions.pop()

    # Step 3: Initialize backtracking
    backtrack([], groups, students)

    # Log statistics
    print(f"Total Recursive Calls: {recursive_calls}")

    # Calculate the final subject hours for each subject
    total_hours_all_divisions = {subject: 0 for subject in total_hours}
    for division in best_solution["divisions"]:
        division_hours = calculate_hours(division)
        for subject in total_hours_all_divisions:
            total_hours_all_divisions[subject] += division_hours[subject]

    # Return the best solution with subject hours included
    return best_solution, total_hours_all_divisions


# Run the revised algorithm
result, subject_hours = allocate_groups_with_splitting(subject_groups, total_hours, min_students, max_students)

print("\nOptimal Division Allocation:")
if result["divisions"]:
    for i, division in enumerate(result["divisions"], start=1):
        division_students = sum(count for _, count in division)
        print(f"Division {i}: {division}, Total Students: {division_students}")

# Print total deviation
print("\nTotal Deviation:", result["deviation"])

# Print the subject hours for each subject in the final solution
print("\nFinal Subject Hours Across All Divisions:")
for subject, hours in subject_hours.items():
    print(f"{subject}: {hours} hours")
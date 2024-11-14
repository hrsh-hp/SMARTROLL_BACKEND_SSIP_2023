### Problem Statement: Optimal Division Assignment of Subjects for Balanced Teaching Hours

**Objective**: Given a set of subjects each with a minimum weekly teaching requirement (in hours), and a set of student groups that select a combination of these subjects, we want to assign student groups to two divisions. The goal is to minimize teaching hours while ensuring each subject meets its minimum weekly requirement across both divisions.

**Inputs**:

1. **Total Hours per Subject**: A dictionary that specifies the minimum teaching hours required per subject each week, e.g.:

   ```python
   total_hours = {
       "ML": 4,
       "BDA": 4,
       "IS": 4,
       "MCWC": 3,
       "CC": 3,
       "MAD": 3,
       "DF": 3,
   }
   ```
2. **Student Groups and Counts**: A dictionary where each key is a tuple representing the subjects chosen by a group of students, and each value is the number of students in that group, e.g.:

   ```python
   student_groups = {
       ('ML', 'IS', 'CC', 'DF'): 69,
       ('BDA', 'IS', 'MCWC', 'MAD'): 11,
       ('BDA', 'IS', 'CC', 'DF'): 78,
       ('BDA', 'IS', 'CC', 'MAD'): 7,
       ('BDA', 'IS', 'MCWC', 'DF'): 13,
   }
   ```

**Requirements**:

- Distribute the student groups across **Division 1** and **Division 2**.
- The final allocation should aim for each subject’s teaching hours across both divisions to meet the minimum required hours in the `total_hours` dictionary.
- If a subject appears in both divisions, its teaching hours are considered met; otherwise, it should meet its minimum hours in one division.

**Expected Outputs**:

1. **Division 1 and Division 2 Assignments**: Two dictionaries listing the groups assigned to each division with their student counts:

   ```python
   Division 1 student groups and counts: {('ML', 'IS', 'CC', 'DF'): 69, ('BDA', 'IS', 'MCWC', 'MAD'): 11}
   Division 2 student groups and counts: {('BDA', 'IS', 'CC', 'DF'): 78, ('BDA', 'IS', 'MCWC', 'DF'): 13}
   ```
2. **Final Teaching Hours per Subject**: A dictionary showing the calculated teaching hours across both divisions, indicating if the minimum requirements are met:

   ```python
   Final teaching hours per subject:
   ML: 4 hours (Minimum required: 4 hours)
   BDA: 8 hours (Minimum required: 4 hours)
   IS: 8 hours (Minimum required: 4 hours)
   MCWC: 6 hours (Minimum required: 3 hours)
   CC: 6 hours (Minimum required: 3 hours)
   MAD: 3 hours (Minimum required: 3 hours)
   DF: 6 hours (Minimum required: 3 hours)
   ```

### Example Problem

Using the above inputs, an optimal solution should distribute groups across the two divisions in a way that each subject meets its minimum hours requirement (by appearing across both divisions or achieving double hours in one division).

### Objectives for Optimizing Division Assignment

1. **Meet Minimum Teaching Hours**: Ensure that each subject's teaching hours across both divisions meet or exceed the required minimum hours specified in the `total_hours` input.
2. **Optimize Distribution**:

   - Distribute student groups in a way that each subject’s total hours are **as close as possible to the required minimum**. Avoid unnecessary excess hours for any subject to ensure efficient use of teaching resources.
3. **Balance Student Distribution**:

   - Aim for a balanced allocation of student groups across both divisions, if possible. This helps prevent overloading one division and ensures each division is equally manageable.
4. **Avoid Redundant Teaching Hours**:

   - If a subject already meets the required teaching hours in one division, avoid assigning additional student groups for the same subject in the same division. Assign those groups to the other division if it helps meet requirements for other subjects more effectively.
5. **Maintain Group Integrity**:

   - Each student group, defined by the combination of subjects they are taking, should be assigned entirely to one division to maintain consistent scheduling and avoid splitting student cohorts.

By focusing on these objectives, the algorithm should produce an optimized division of student groups that minimizes teaching hours while meeting all subject requirements efficiently.

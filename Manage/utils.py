from Manage.models import Lecture,Schedule
from pywebpush import webpush, WebPushException
import json
from django.conf import settings
from datetime import datetime
import re
import hashlib

def send_notification_async(time):
    current_datetime = datetime.now()
    current_day_name = current_datetime.strftime('%A')
    schedules = Schedule.objects.filter(day=current_day_name.lower())
    for day in schedules:
        lectures = Lecture.objects.filter(schedule=day,start_time=time)         
        for lecture in lectures:
            if lecture.teacher.web_push_subscription:
                subscriptions = lecture.teacher.web_push_subscription.all()
                for subscription in subscriptions:
                    try:
                        notification_body=f"You have a session scheduled at {lecture.start_time} for {lecture.subject.subject_name} | Semester - {lecture.subject.semester.no} at {lecture.classroom.class_name}"                        
                        webpush(subscription_info=json.loads(subscription.subscription),data=notification_body,vapid_private_key=settings.VAPID_PRIVATE_KEY,vapid_claims=settings.VAPID_CLAIMS)
                    except WebPushException as e:
                        print(e)
# Regexes
BE_PATTERN = re.compile(r"^(BE)-(\d+)-([A-Z])(?:_([A-Z]\d))?-([A-Z]+(?:-\w+)?)-(\w+)$")
ME_PATTERN = re.compile(r"^(ME)-(\d+)-([A-Z]+(?:-\w+)?)-(\d+)$")
TIME_PATTERN = re.compile(r"^(\d{2}:\d{2})-(\d{2}:\d{2})$")
                

def parse_be_me_string(string):
    # Try BE pattern first
    be_match = BE_PATTERN.match(string)
    if be_match:
        course, sem, div, batch, sub, classroom = be_match.groups()
        return {
            "stream": course,
            "sem": sem,
            "div": div,
            "batch": batch if batch else None,  # If no batch, set to None
            "sub": sub,
            "classroom": classroom
        }
    
    # Try ME pattern
    me_match = ME_PATTERN.match(string)
    if me_match:
        course, sem, sub, classroom = me_match.groups()
        return {
            "stream": course,
            "sem": sem,
            "sub": sub,
            "classroom": classroom
        }
    if string !='RECESS' and len(string.strip()) > 0:        
        raise Exception(f'Invalid lecture format found!! {string}')
    # If no pattern matches
    return None

def parse_time_string(time_string):
    time_match = TIME_PATTERN.match(time_string)
    if time_match:
        start_time, end_time = time_match.groups()
        return {"start_time": start_time, "end_time": end_time}    
    if time_string !='RECESS':raise Exception('Invalid time format found!!')
    return None

def hash_string(input_string):
    # Convert the string to bytes
    byte_string = input_string.encode()
    # Create a SHA-256 hash of the byte string
    hash_object = hashlib.sha256(byte_string)
    # Return the hex representation of the hash
    return hash_object.hexdigest()

def check_for_batch_includance(subject_obj,batches):    
    allowed_batches = []
    for batch in batches:
        if subject_obj.included_batches.contains(batch):
            allowed_batches.append(batch)
    return allowed_batches

def allocate_groups_with_splitting(subject_groups, total_hours, min_students, max_students):
    # Step 1: Preprocess subject groups to split any group exceeding max_students
    preprocessed_groups = []
    for group, students in subject_groups.items():
        student_list = list(students)  # Convert to a list if necessary
        while len(student_list) > max_students:
            preprocessed_groups.append((group, student_list[:max_students]))
            student_list = student_list[max_students:]
        if len(student_list) > 0:
            preprocessed_groups.append((group, student_list))

    # Step 2: Initialize variables for the backtracking algorithm
    groups = [group for group, _ in preprocessed_groups]
    students = [students for _, students in preprocessed_groups]
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

    def backtrack(current_divisions, remaining_groups, remaining_students):
        nonlocal recursive_calls
        recursive_calls += 1

        # Base case: no groups left to allocate
        if not remaining_groups:
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

        # Recursive case: allocate the next group
        group = remaining_groups[0]
        group_students = remaining_students[0]
        count = len(group_students)

        # Try allocating the group (or part of it) to each division
        for i in range(len(current_divisions)):
            division = current_divisions[i]
            division_student_count = sum(len(students) for _, students in division)

            if division_student_count + count <= max_students:
                # Allocate the entire group to this division
                division.append((group, group_students))
                backtrack(current_divisions, remaining_groups[1:], remaining_students[1:])
                division.pop()
            else:
                # Allocate a part of the group to this division
                split_count = max_students - division_student_count
                if split_count > 0:
                    division.append((group, group_students[:split_count]))
                    backtrack(
                        current_divisions,
                        [group] + remaining_groups[1:],
                        [group_students[split_count:]] + remaining_students[1:],
                    )
                    division.pop()

        # Start a new division with this group
        if len(current_divisions) < len(groups):
            current_divisions.append([(group, group_students)])
            backtrack(current_divisions, remaining_groups[1:], remaining_students[1:])
            current_divisions.pop()

    # Step 3: Initialize backtracking
    backtrack([], groups, students)
    # Log statistics
    # print(f"Total Recursive Calls: {recursive_calls}")
    # Calculate the final subject hours for each subject
    total_hours_all_divisions = {subject: 0 for subject in total_hours}
    for division in best_solution["divisions"]:
        division_hours = calculate_hours(division)
        for subject in total_hours_all_divisions:
            total_hours_all_divisions[subject] += division_hours[subject]

    # Return the best solution with subject hours included
    return best_solution, total_hours_all_divisions

# Generate short form
def generate_short_form(subject):
    if type(subject) == str:
        return subject
    words = subject.subject_map.subject_name.split()
    short_form = ''.join(word[0] for word in words if word[0].isalpha()).upper()
    return short_form

def create_batches(subject, students, max_batch_size=24, single_batch_threshold=34):
    batches = {}
    students_list = list(students)  # Convert set to sorted list
    count = len(students_list)
    subject_shortform = generate_short_form(subject)
    
    if count <= single_batch_threshold:
        # Single batch case
        batches[f"{subject_shortform}1"] = students_list
    else:
        # Multiple batch case
        num_batches = max(1, (count + max_batch_size - 1) // max_batch_size)
        # Try to minimize the number of batches
        while True:
            base_size = count // num_batches
            extra = count % num_batches
            
            if base_size <= max_batch_size:
                break
            num_batches += 1
        
        # Distribute students across batches
        batch_sizes = [base_size + 1 if i < extra else base_size for i in range(num_batches)]
        start_index = 0
        
        for i, size in enumerate(batch_sizes, start=1):
            end_index = start_index + size
            batches[f"{subject_shortform}{i}"] = students_list[start_index:end_index]
            start_index = end_index

    return batches
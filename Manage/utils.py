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
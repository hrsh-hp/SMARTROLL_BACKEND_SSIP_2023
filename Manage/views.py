from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from django.http import JsonResponse
from Manage.models import Division, Semester,Batch,TimeTable,Schedule,Classroom,Lecture,Term,Link,Stream,PermanentSubject,Semester,Subject,Branch,College,Term,Stream,ComplementrySubjects,SubjectChoices,SubjectGroups
from StakeHolders.models import Admin,Teacher,Student,NotificationSubscriptions,SuperAdmin
from Profile.models import Profile
from .serializers import SemesterSerializer,DivisionSerializer,BatchSerializer,SubjectSerializer,TimeTableSerializer,ClassRoomSerializer,LectureSerializer,TermSerializer,TimeTableSerializerForTeacher,TimeTableSerializerForStudent,LectureSerializerForHistory,BranchWiseTimeTableSerializer,BranchWiseTimeTableSerializerStudent,BranchSerializer,StreamSerializer,PermanentSubjectSerializer,SemesterSerializerByStream,ComplementrySubjectsSerializer,FinalizedSubjectChoicesSerializer,SemesterOnlySerializerByStream,SubjectGroupSerializer
from Session.models import Session,Attendance
import pandas as pd
from django.contrib.auth import get_user_model
from StakeHolders.serializers import TeacherSerializer,StudentSerializer
import datetime
from django.conf import settings as django_settings
import os
from django.core.mail import send_mail
from threading import Thread
from .utils import parse_be_me_string,parse_time_string,hash_string,check_for_batch_includance,allocate_groups_with_splitting,generate_short_form,create_batches
import json
from SMARTROLL.GlobalUtils import generate_unique_hash
from django.db import transaction
from django.db.models import Count, Q
import string
from django.core.cache import cache

# Create your views here.

User = get_user_model()

def send_activation_email(receiver,teacher_slug,host):    
    sender_email = django_settings.EMAIL_HOST_USER
    sent = False
    url = f'http://{host}/teacher_activation/{teacher_slug}'
    try:
        send_mail('Activate Your Acount',url, from_email=sender_email,recipient_list=[receiver])
        sent=True
    except Exception as e:             
        sent = False
    return sent


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_active_terms_for_superadmin(request):
    try:        
        if request.user.role == 'superadmin':
            data = {'data':None,'error':False,'message':None}
            superadmin_obj = SuperAdmin.objects.filter(profile=request.user).first()
            if superadmin_obj:
                # Get the branches controlled by superadmin                
                terms = Term.objects.filter(college__super_admins=superadmin_obj)
                terms_serialized = TermSerializer(terms,many=True)
                data['data'] = terms_serialized.data                
                return JsonResponse(data,status=200)
            else:
                raise Exception("Superadmin does not exists!!")
        else: 
            raise Exception("You're not allowed to perform this action")
            
    except Exception as e:
        print(e)
        data = {"data":str(e)}
        return JsonResponse(data,status=500)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_object_counts(request):    
    try:        
        if request.user.role == 'admin':
            data = {'streams':0,'semesters':0,'divisons':0,'batches':0}
            admin_obj = Admin.objects.get(profile=request.user)
            # We'll have to get the counts of semester, divisions, batches
            # branch = admin_obj.branch_set.first()
            # term_count = len(term)
            streams = Stream.objects.filter(branch__admins=admin_obj)
            stream_count = len(streams)
            print(streams)
            semesters = []
            for i in streams:
                stream_sems = i.semester_set.all()
                semesters.extend(stream_sems)
            semester_count = len(semesters)
            divisions = []
            for i in semesters:
                sem_divs = i.division_set.all()
                divisions.extend(sem_divs)
            division_count = len(divisions)
            batches = []
            for i in divisions:
                div_batches = i.batch_set.all()
                batches.extend(div_batches)
            batch_count = len(batches)    
            data['streams'] = stream_count
            data['semesters'] = semester_count
            data['divisons'] = division_count
            data['batches'] = batch_count
            return JsonResponse(data,status=200)
        else:
            raise Exception("You're not allowed to perform this action")
    except Exception as e:
        print(e)
        data = {"data":str(e)}
        return JsonResponse(data,status=500)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_term(request):
    try:        
        data = {'data':None,'error':False,'message':None}
        if request.user.role == 'superadmin':  
            body = request.data
            if 'start_year' in body and 'end_year' in body :
                superadmin_obj = SuperAdmin.objects.get(profile=request.user)
                # We'll have to get the counts of semester, divisions, batches
                college_obj = superadmin_obj.college_set.first()
                if college_obj:
                    term_obj,created = Term.objects.get_or_create(start_year=body['start_year'],end_year=body['end_year'],college=college_obj)
                    if created:
                        # Deactivate all the previous terms
                        old_terms = college_obj.term_set.all().exclude(id=term_obj.id)
                        for term in old_terms:
                            term.status = False
                            term.save()
                        # Now activate the current term                        
                        term_obj.status=True
                        term_obj.save()
                        term_serialized = TermSerializer(term_obj)
                        data['data'] = term_serialized.data
                        return JsonResponse(data,status=200)
                    else:
                        raise Exception('Term already added')
                else:
                    raise Exception('No branch found')
            else:
                raise Exception('Provide all the parameters')                        
        else:
            raise Exception("You're not allowed to perform this action")
    except Exception as e:
        print(e)
        data['error'] = True
        data['message'] = str(e)
        return JsonResponse(data,status=500) 

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_terms(request):    
    try:        
        data = {'data':None,'error':False,'message':None}
        body = request.query_params
        if request.user.role == 'superadmin':              
            superadmin_obj = SuperAdmin.objects.get(profile=request.user)
            # We'll have to get the counts of semester, divisions, batches
            college_obj = superadmin_obj.college_set.first()
            terms = college_obj.term_set.all()
            if terms.exists():
                terms_serialized = TermSerializer(terms,many=True)
                data['data'] = terms_serialized.data
                return JsonResponse(data,status=200)
            else:
                raise Exception('No Term Added')
        else:
            raise Exception("You're not allowed to perform this action")
    except Exception as e:
        print(e)
        data['error'] = True
        data['message'] = str(e)   
        return JsonResponse(data,status=500)   

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_semester(request):
    try:        
        data = {'data':None,'error':False,'message':None}
        if request.user.role == 'admin':
            body = request.data
            if 'no' in body and 'term_slug' in body:
                admin_obj = Admin.objects.get(profile=request.user)
                # We'll have to get the counts of semester, divisions, batches
                term_obj = Term.objects.filter(slug=body['term_slug']).first()
                if term_obj:
                    semester_obj,created = Semester.objects.get_or_create(no=body['no'],term=term_obj)
                    if created:                                                
                        semester_serialized = SemesterSerializer(semester_obj)
                        data['data'] = semester_serialized.data
                        return JsonResponse(data,status=200)
                    else:
                        raise Exception('Semester already added')
                else:
                    raise Exception('No branch found')
            else:
                raise Exception('Provide all the parameters')                        
        else:
            raise Exception("You're not allowed to perform this action")
    except Exception as e:
        print(e)
        data['error'] = True
        data['message'] = str(e)
        return JsonResponse(data,status=500)    
        

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_semesters(request):
    try:        
        data = {'data':None,'error':False,'message':None}
        body = request.query_params
        if request.user.role == 'admin':
            admin_obj = Admin.objects.get(profile=request.user)
            if 'stream_slug' in body:
                # We'll have to get the counts of semester, divisions, batches
                stream_obj = Stream.objects.filter(slug=body['stream_slug']).first()
                if stream_obj:
                    semesters = stream_obj.semester_set.all().filter(status=True)
                    if semesters.exists():
                        semesters_serialized = SemesterSerializer(semesters,many=True)
                        data['data'] = semesters_serialized.data
                        return JsonResponse(data,status=200)
                    else:
                        raise Exception('Semester Does Not Exists')
                else:
                        raise Exception('Stream Does Not Exists')
            else:
                raise Exception('Parameters missing')
        else:
            raise Exception("You're not allowed to perform this action")
    except Exception as e:
        print(e)
        data['error'] = True
        data['message'] = str(e)   
        return JsonResponse(data,status=500) 
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_division(request):
    try:    
        data = {'data':None,'error':False,'message':None}    
        if request.user.role == 'admin':
            body = request.data
            admin_obj = Admin.objects.get(profile=request.user)            
            if 'division_name' in body and 'semester_slug' in body and len(body['division_name']) > 0:
                semester_obj = Semester.objects.filter(slug=body['semester_slug']).first()                
                if semester_obj and semester_obj.stream.branch.admins.contains(admin_obj):
                    division_obj,created = Division.objects.get_or_create(division_name = body['division_name'],semester=semester_obj)
                    if created:
                        division_serialized = DivisionSerializer(division_obj)
                        timetable_obj = TimeTable.objects.create(division=division_obj)
                        days = ['MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY']
                        for day in days:
                            Schedule.objects.create(day=day, timetable=timetable_obj)
                        data['data'] = division_serialized.data
                        return JsonResponse(data,status=200)
                    else:
                        raise Exception('division already added')
                else:
                    raise Exception("This Semester does not exist")
            else:
                raise Exception("Credentials not provided")
            
        else:
            raise Exception("You're not allowed to perform this action")
    except Exception as e:
        print(e)
        data['message'] = str(e)
        data['error'] = True        
        return JsonResponse(data,status=500)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_batch(request):
    try:    
        data = {'data':None,'error':False,'message':None}    
        if request.user.role == 'admin':
            body = request.data
            admin_obj = Admin.objects.get(profile=request.user)            
            if 'batch_name' in body and 'division_slug' in body and len(body['batch_name']) > 0:
                division_obj = Division.objects.filter(slug=body['division_slug']).first()                
                if division_obj and division_obj.semester.stream.branch.admins.contains(admin_obj):
                    batch_obj,created = Batch.objects.get_or_create(batch_name = body['batch_name'],division=division_obj)
                    if created:
                        batch_serialized = BatchSerializer(batch_obj)
                        data['data'] = batch_serialized.data
                        return JsonResponse(data,status=200)
                    else:
                        raise Exception('Batch already added')
                else:
                    raise Exception("This Semester does not exist")
            else:
                raise Exception("Credentials not provided")
            
        else:
            raise Exception("You're not allowed to perform this action")
    except Exception as e:
        print(e)
        data['message'] = str(e)
        data['error'] = True        
        return JsonResponse(data,status=500)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_batches(request):
    try:    
        data = {'data':None,'error':False,'message':None}    
        if request.user.role == 'admin':
            body = request.query_params
            admin_obj = Admin.objects.get(profile=request.user)
            if 'division_slug' in body :
                division_obj = Division.objects.filter(slug=body['division_slug']).first()
                if division_obj and division_obj.semester.stream.branch.admins.contains(admin_obj):
                   batches = division_obj.batch_set.all()
                   batches_serialized = BatchSerializer(batches,many=True)
                   data['data'] = batches_serialized.data
                   return JsonResponse(data,status=200)
                else:
                   raise Exception('Divison does not exist')
            else:
                raise Exception("Credentials not provided")
        else:
            raise Exception("You're not allowed to perform this action")
    except Exception as e:
        print(e)
        data['message'] = str(e)
        data['error'] = True        
        return JsonResponse(data,status=500)
        
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_divisions(request):
    try:    
        data = {'data':None,'error':False,'message':None}    
        if request.user.role == 'admin':
            body = request.query_params
            admin_obj = Admin.objects.get(profile=request.user)
            # We'll have to get the counts of semester, divisions, batches
            if 'semester_slug' in body:
                semester_obj = Semester.objects.filter(slug=body.get('semester_slug')).first()
                if semester_obj and semester_obj.stream.branch.admins.contains(admin_obj):
                    divisions = semester_obj.division_set.all()
                    division_serialized = DivisionSerializer(divisions, many=True)
                    data['data'] = division_serialized.data
                    return JsonResponse(data,status=200)
                else:
                    raise Exception("This Semester does not exist")
            else:
                raise Exception("Choose the correct semester to get the divisions")            
            
        else:
            raise Exception("You're not allowed to perform this action")
    except Exception as e:
        print(e)
        data['message'] = str(e)
        data['error'] = True
        return JsonResponse(data,status=500)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_subject(request):
    try:        
        data = {'data':None,'error':False,'message':None}
        if request.user.role == 'admin':  
            body = request.data
            admin_obj = Admin.objects.get(profile=request.user)       
            if 'code' in body and 'subject_name' in body and 'short_name' in body and 'credit' in body and 'semester_slug' in body and 'batches' in body:
                semester_obj = Semester.objects.filter(slug= body['semester_slug']).first()
                if semester_obj and semester_obj.stream.branch.admins.contains(admin_obj):
                    subject_obj,created = Subject.objects.get_or_create(code=body['code'],subject_name = body['subject_name'], short_name=body['short_name'],credit = body['credit'],semester = semester_obj)
                    if created:                        
                        batches = Batch.objects.filter(slug__in=body['batches'])
                        subject_obj.included_batches.add(*batches)
                        subject_serialized = SubjectSerializer(subject_obj)
                        data['data'] = subject_serialized.data
                        return JsonResponse(data,status=200)
                    else:
                        raise Exception("Subject is already exist")
                else:
                    raise Exception("Semester does not exist")
            else:
                raise Exception("Provide the proper credentials")        
        else:
            raise Exception("You're not allowed to perform this action")            

    except Exception as e:
        print(e)
        data['message'] = str(e)
        data['error'] = True
        return JsonResponse(data,status=500)    
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_subjects(request):
    try:    
        data = {'data':None,'error':False,'message':None}    
        if request.user.role == 'admin':            
            admin_obj = Admin.objects.get(profile=request.user)                                    
            branch_obj = admin_obj.branch_set.first()            
            subjects = Subject.objects.filter(semester__stream__branch=branch_obj)
            subject_serialized = SubjectSerializer(subjects, many=True)
            data['data'] = subject_serialized.data
            return JsonResponse(data,status=200)
        else:
            raise Exception("You're not allowed to perform this action")
    except Exception as e:        
        print(e)
        data['message'] = str(e)
        data['error'] = True
        return JsonResponse(data,status=500)
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_teacher(request):
    try:    
        data = {'data':None,'error':False,'message':None}    
        if request.user.role == 'admin':
            body = request.data
            admin_obj = Admin.objects.get(profile=request.user)            
            branch_obj = admin_obj.branch_set.first()
            if 'name' in body and 'email' in body:
                profile_obj,created = Profile.objects.get_or_create(name=body['name'],email=body['email'],role='teacher')
                if created:
                    teacher_obj = Teacher.objects.create(profile=profile_obj)
                    branch_obj.teachers.add(teacher_obj)
                    teacher_serialized = TeacherSerializer(teacher_obj)
                    Thread(target=send_activation_email,args=(body['email'],teacher_obj.slug,request.META['HTTP_HOST'])).start()
                    data['data'] = teacher_serialized.data
                    return JsonResponse(data,status=200)
                else:
                    raise Exception('Teacher is already added, Please check the mail!!')
            else:
                raise Exception('Credentials not provided')
        else:
            raise Exception("You're not allowed to perform this action")
    except Exception as e:
        print(e)
        data['message'] = str(e)
        data['error'] = True        
        return JsonResponse(data,status=500)
    
@api_view(['POST'])
def activate_teacher_acount(request):
    try:
        data = {'data':None,'error':False,'message':None}
        body = request.data
        if 'password' in body and 'teacher_slug' in body:
            teacher_obj = Teacher.objects.filter(slug=body['teacher_slug']).first()
            if teacher_obj:                
                if not teacher_obj.profile.is_active:
                    teacher_obj.profile.is_active = True
                    teacher_obj.profile.set_password(body['password'])
                    teacher_obj.profile.save()
                    data['data'] = True
                    return JsonResponse(data,status=200)
                else:
                    raise Exception('Teacher is already added')
            else:
                raise Exception('Teacher does not exists')
        else:
            raise Exception('Parameters missing')
    except Exception as e:
        print(e)
        data['message'] = str(e)
        data['error'] = True        
        return JsonResponse(data,status=500)
    
@api_view(['POST'])
def set_new_password_for_student(request):
    try:
        data = {'data':None,'error':False,'message':None}
        body = request.data
        if 'password' in body and 'student_slug' in body:
            student_obj = Student.objects.filter(slug=body['student_slug']).first()            
            if not student_obj:                
                raise Exception('Student does not exists')
            student_obj.profile.set_password(body['password'])               
            data['data'] = True
            return JsonResponse(data,status=200)
        else:
            raise Exception('Parameters missing')
    except Exception as e:
        print(e)
        data['message'] = str(e)
        data['error'] = True        
        return JsonResponse(data,status=500)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_teachers(request):
    try: 
        data = {'data':None,'error':False,'message':None}    
        if request.user.role == 'admin':            
            admin_obj = Admin.objects.get(profile=request.user)            
            branch_obj = admin_obj.branch_set.first()
            teachers = branch_obj.teachers.all()
            teacher_serialized = TeacherSerializer(teachers,many=True)
            data['data'] = teacher_serialized.data
            return JsonResponse(data,status=200)
        else:
            raise Exception("You're not allowed to perform this action")
    except Exception as e:
        print(e)
        data['message'] = str(e)
        data['error'] = True        
        return JsonResponse(data,status=500)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_timetable(request,division_slug):
    try:    
        data = {'data':None,'error':False,'message':None}    
        if request.user.role == 'admin':                        
            division_obj = Division.objects.filter(slug=division_slug).first()
            timetable_obj = TimeTable.objects.filter(division=division_obj).first()
            if timetable_obj:
                timetable_serialized = TimeTableSerializer(timetable_obj)
                data['data'] = timetable_serialized.data
                return JsonResponse(data,status=200)
            else:
                raise Exception('No timetable exists for this division')
        else:
            raise Exception("You're not allowed to perform this action")
    except Exception as e:
        print(e)
        data['message'] = str(e)
        data['error'] = True        
        return JsonResponse(data,status=500)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_lecture_configs(request):
    try:
        data = {'data':None,'error':False,'message':None}
        if request.user.role == 'admin':
            body = request.query_params
            admin_obj = Admin.objects.get(profile=request.user)
            branch_obj = admin_obj.branch_set.first()
            if 'schedule_slug' in body:
                schedule_obj = Schedule.objects.filter(slug=body['schedule_slug']).first()
                division_obj = Division.objects.filter(timetable__schedule = schedule_obj).first()
                semester_obj = division_obj.semester
                if division_obj and semester_obj and schedule_obj: 
                    teachers = branch_obj.teachers.all()
                    classrooms = branch_obj.classroom_set.all()                    
                    subjects = Subject.objects.filter(semester = semester_obj)
                    teachers_serialized = TeacherSerializer(teachers,many=True)
                    classrooms_serialized = ClassRoomSerializer(classrooms,many=True)                    
                    subjects_serialized = SubjectSerializer(subjects,many=True)
                    data['data'] = {}
                    data['data']['teachers'] = teachers_serialized.data
                    data['data']['classrooms'] = classrooms_serialized.data                    
                    data['data']['subjects'] = subjects_serialized.data
                    return JsonResponse(data,status=200)
                else:
                    raise Exception('Object Not Found')
            else:
                raise Exception('Parameters missing')
        else:
            raise Exception("You're not allowed to perform this action")
    except Exception as e:
        print(e)
        data['message'] = str(e)
        data['error'] = True        
        return JsonResponse(data,status=500)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_lecture_to_schedule(request):
    try:
        data = {'data':None,'error':False,'message':None}
        if request.user.role == 'admin':
            body = request.data
            if "schedule_slug" in body and "start_time" in body and "end_time" in body and "type" in body and "subject" in body and "teacher" in body and "classroom" in body and "batches" in body:
                schedule = Schedule.objects.get(slug=body['schedule_slug'])
                start_time  = datetime.datetime.strptime(body['start_time'], "%H:%M").time()
                end_time  = datetime.datetime.strptime(body['end_time'], "%H:%M").time()
                subject = Subject.objects.get(slug=body['subject'])
                teacher = Teacher.objects.get(slug=body['teacher'])
                classroom = Classroom.objects.get(slug=body['classroom'])
                lecture_obj,created = Lecture.objects.get_or_create(start_time=start_time,end_time=end_time,schedule=schedule)
                if created:
                    lecture_obj.type=body['type']
                    lecture_obj.subject=subject
                    lecture_obj.teacher=teacher
                    lecture_obj.classroom=classroom
                    lecture_obj.save()
                    batches = Batch.objects.filter(slug__in=body['batches'])
                    lecture_obj.batches.add(*batches)
                    # Need to create lecture sessions for this particular lecture...after that the cronjob will take care of it
                    today = datetime.datetime.now().date()                    
                    if lecture_obj:
                            batches = lecture_obj.batches.all()
                            lecture_session,created = Session.objects.get_or_create(lecture=lecture_obj,day=today,active='pre')
                            if created:             
                                students = Student.objects.filter(batch__in=batches)
                                for student in students:
                                    attendance_obj = Attendance.objects.create(student=student)
                                    lecture_session.attendances.add(attendance_obj)
                    else:
                        raise Exception('Lecture does not exists')
                    lecture_obj_serialized = LectureSerializer(lecture_obj)
                    data['data'] = lecture_obj_serialized.data
                    return JsonResponse(data,status=200)
                else:
                    raise Exception('Lecture already exists for this timeslot')
            else:
                raise Exception('Credentials Missing')               
        else:
            raise Exception("You're not allowed to perform this action")
    except Exception as e:
        print(e)
        data['message'] = str(e)
        data['error'] = True        
        return JsonResponse(data,status=500)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_lecture_as_proxy(request):
    try:
        data = {'data':None,'error':False,'message':None}
        if request.user.role == 'admin':
            body = request.data
            if "prev_lecture_slug" in body and "schedule_slug" in body and "start_time" in body and "end_time" in body and "type" in body and "subject" in body and "teacher" in body and "classroom" in body and "batches" in body:
                prev_lecture_obj = Lecture.objects.filter(slug=body['prev_lecture_slug']).first()
                print(prev_lecture_obj)
                if prev_lecture_obj:
                    schedule = Schedule.objects.get(slug=body['schedule_slug'])
                    start_time  = datetime.datetime.strptime(body['start_time'], "%H:%M").time()
                    end_time  = datetime.datetime.strptime(body['end_time'], "%H:%M").time()
                    subject = Subject.objects.get(slug=body['subject'])
                    teacher = Teacher.objects.get(slug=body['teacher'])
                    classroom = Classroom.objects.get(slug=body['classroom'])
                    lecture_obj,created = Lecture.objects.get_or_create(start_time=start_time,end_time=end_time,schedule=schedule,is_proxy = True)
                    if created:
                        # Create link object 
                        link_obj,created = Link.objects.get_or_create(from_lecture=prev_lecture_obj,to_lecture=lecture_obj)
                        lecture_obj.type=body['type']
                        lecture_obj.subject=subject
                        lecture_obj.teacher=teacher
                        lecture_obj.classroom=classroom
                        lecture_obj.save()
                        batches = Batch.objects.filter(slug__in=body['batches'])
                        lecture_obj.batches.add(*batches)
                        # Need to create lecture sessions for this particular lecture till the next sunday...after that the cronjob will take care of it
                        today = datetime.datetime.now().date()                    
                        if lecture_obj:
                                batches = lecture_obj.batches.all()
                                lecture_session,created = Session.objects.get_or_create(lecture=lecture_obj,day=today,active='pre')
                                if created:           
                                    students = Student.objects.filter(batch__in=batches)
                                    for student in students:
                                        attendance_obj = Attendance.objects.create(student=student)
                                        lecture_session.attendances.add(attendance_obj)
                        else:
                            raise Exception('Lecture does not exists')
                        lecture_obj_serialized = LectureSerializer(lecture_obj)
                        data['data'] = lecture_obj_serialized.data
                        return JsonResponse(data,status=200)
                    else:
                        raise Exception('Lecture already exists for this timeslot')
                else:
                    raise Exception('Lecture does not exists')
            else:
                raise Exception('Credentials Missing')               
        else:
            raise Exception("You're not allowed to perform this action")
    except Exception as e:
        print(e)
        data['message'] = str(e)
        data['error'] = True        
        return JsonResponse(data,status=500)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_students_data(request):
    try:
        data = {'data':{'logs':{},'register_count':0,'error_count':0},'error':False,'message':None}
        if request.user.role == 'admin':
            body = request.data
            admin_obj = Admin.objects.get(profile=request.user)              
            if 'sheet_name' in body and 'division_slug' in body and 'students.xlsc' in body and 'stream_slug' in body:
                stream_obj = admin_obj.branch_set.first().stream_set.filter(slug=body['stream_slug']).first()
                divison_obj = Division.objects.filter(slug=body['division_slug']).first()
                if divison_obj:
                    df = pd.read_excel(body['students.xlsc'],sheet_name=body['sheet_name'])
                    df = df.drop(index=range(3))
                    current_batch = None                         
                    for index,row in df.iterrows():    
                        try:
                            if not pd.isna(row[0]):
                                serial_no = row[0]
                                batch = row[1] if not pd.isna(row[1]) else current_batch
                                current_batch = batch
                                enrollment = row[2]
                                name = row[3]
                                gender = row[4]                                
                                batch_obj = divison_obj.batch_set.filter(batch_name=batch).first()
                                if batch_obj:
                                    student_obj,student_created = Student.objects.get_or_create(enrollment=enrollment)
                                    if student_created:
                                        profile_obj,created = Profile.objects.get_or_create_by_name(name=name,role='student')
                                        print(profile_obj)
                                        student_obj.profile = profile_obj
                                        student_obj.save()
                                    if not batch_obj.students.contains(student_obj) : batch_obj.students.add(student_obj)
                                    if not stream_obj.students.contains(student_obj) : stream_obj.students.add(student_obj)
                                    data['data']['register_count'] += 1
                                    data['data']['logs'][serial_no] = f"Student Created - {serial_no} - {batch[1:]} - {enrollment} - {name} - {gender}"
                                else:
                                    raise Exception(f"Batch/Division does not exist for {serial_no} - {batch[1:]} - {enrollment} - {name} - {gender}")                        
                        except Exception as e:
                            print(e)
                            data['data']['error_count'] += 1
                            data['data']['logs'][row[0]] = f"{str(e)} - {serial_no} - {batch[1:]} - {enrollment} - {name} - {gender}"
                    return JsonResponse(data,status=200)
                else:
                    raise Exception('Division not found')
            else:
                raise Exception('Parameters missing')
        else:
            raise Exception("You're not allowed to perform this action")
    except Exception as e:
        print(e)
        data['message'] = str(e)
        data['error'] = True        
        return JsonResponse(data,status=500)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_timetable_for_teacher(request):
    try:
        data = {'data':None,'error':False,'message':None}
        if request.user.role == 'teacher':
            teacher_obj = Teacher.objects.filter(profile=request.user).first()
            if teacher_obj:                                
                branches = teacher_obj.branch_set.all()
                timetables_serialized = BranchWiseTimeTableSerializer(instance=branches,teacher=teacher_obj,many=True)
                # for branch in branches:                    
                #     branch.semesters = branch.term_set.filter(status=True).first().semester_set.filter(status=True)
                #     divisions = Division.objects.filter(semester__in=branch.semesters)
                #     timetables = TimeTable.objects.filter(division__in=divisions)
                #     timetable_serialized = TimeTableSerializerForTeacher(instance=timetables,teacher=teacher_obj,many=True)
                #     timetables_list.append(timetable_serialized.data)
                data['data'] = timetables_serialized.data
                return JsonResponse(data,status=200)
            else:
                raise Exception('Teacher does not exist')
        else:
            raise Exception("You're not allowed to perform this action")

    except Exception as e:
        print(e)
        data['message'] = str(e)
        data['error'] = True        
        return JsonResponse(data,status=500)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_timetable_for_student(request):
    try:
        data = {'data':{'logs':{},'register_count':0,'error_count':0},'error':False,'message':None}
        if request.user.role == 'student':
            student_obj = Student.objects.filter(profile=request.user).first()
            if student_obj:
                streams = student_obj.stream_set.all()
                branches = [stream.branch for stream in streams]
                timetable_serialized = BranchWiseTimeTableSerializerStudent(instance = branches,many=True,student=student_obj)
                data['data'] = timetable_serialized.data
                return JsonResponse(data,status=200)
            else:
                raise Exception("Student does not exist")
        else:
            raise Exception("You're not allowed to perform this action")

    except Exception as e:
        print(e)
        data['message'] = str(e)
        data['error'] = True        
        return JsonResponse(data,status=500)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_subjects_of_teacher_by_admin(request):
    try:
        data = {'data':None,'error':False,'message':None}
        body = request.query_params        
        if request.user.role == 'admin':
            if 'teacher_slug' not in body:
                raise Exception('Parameters missing')
            teacher_obj = Teacher.objects.filter(slug=body['teacher_slug']).first()
            if teacher_obj:
                lectures = Lecture.objects.filter(teacher=teacher_obj)
                if not lectures:
                    raise Exception(f"No sessions are yet conducted by {teacher_obj.profile.name}")
                subjects = list({lecture.subject for lecture in lectures})
                subjects_serialized = SubjectSerializer(subjects,many=True)
                data['data'] = subjects_serialized.data
                return JsonResponse(data,status=200)
            else:
                raise Exception("Teacher does not exist")
        else:
            raise Exception("You're not allowed to perform this action")

    except Exception as e:
        print(e)
        data['message'] = str(e)
        data['error'] = True        
        return JsonResponse(data,status=500)
        
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_subjects_of_teacher(request):
    try:
        data = {'data':None,'error':False,'message':None}
        if request.user.role == 'teacher':
            teacher_obj = Teacher.objects.filter(profile=request.user).first()
            if teacher_obj:
                subjects = Subject.objects.filter(lecture__teacher=teacher_obj).distinct()
                subjects_serialized = SubjectSerializer(subjects,many=True)
                data['data'] = subjects_serialized.data
                return JsonResponse(data,status=200)
            else:
                raise Exception("Teacher does not exist")
        else:
            raise Exception("You're not allowed to perform this action")

    except Exception as e:
        print(e)
        data['message'] = str(e)
        data['error'] = True        
        return JsonResponse(data,status=500)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_lecture_sessions_for_teacher(request):
    try:
        data = {'data':None,'error':False,'message':None}
        body = request.query_params
        if request.user.role == 'teacher':
            teacher_obj = Teacher.objects.filter(profile=request.user).first()
            if teacher_obj:
                if 'subject_slug' in body:
                        subject_obj = Subject.objects.filter(slug=body['subject_slug']).first()
                        if subject_obj:
                            lectures = subject_obj.lecture_set.filter(teacher=teacher_obj,session__active='post')
                            lectures_serialized = LectureSerializerForHistory(lectures,many=True)
                            data['data'] = lectures_serialized.data
                            return JsonResponse(data,status=200)                            
                        else:
                            raise Exception('Subject does not exists')
                else:
                    raise Exception('Parameters Missing')
            else:
                raise Exception("Teacher does not exist")
        else:
            raise Exception("You're not allowed to perform this action")

    except Exception as e:
        print(e)
        data['message'] = str(e)
        data['error'] = True        
        return JsonResponse(data,status=500)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_lecture_sessions_for_teacher_by_admin(request):
    try:
        data = {'data':None,'error':False,'message':None}
        body = request.query_params
        if request.user.role == 'admin':
            if 'teacher_slug' not in body:
                raise Exception("Parameters missing")
            teacher_obj = Teacher.objects.filter(slug=body['teacher_slug']).first()
            if teacher_obj:
                if 'subject_slug' in body:
                        subject_obj = Subject.objects.filter(slug=body['subject_slug']).first()
                        if subject_obj:
                            lectures = subject_obj.lecture_set.filter(teacher=teacher_obj,session__active='post')
                            lectures_serialized = LectureSerializerForHistory(lectures,many=True)
                            data['data'] = lectures_serialized.data
                            return JsonResponse(data,status=200)                            
                        else:
                            raise Exception('Subject does not exists')
                else:
                    raise Exception('Parameters Missing')
            else:
                raise Exception("Teacher does not exist")
        else:
            raise Exception("You're not allowed to perform this action")

    except Exception as e:
        print(e)
        data['message'] = str(e)
        data['error'] = True        
        return JsonResponse(data,status=500)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def set_web_push_subscription(request):
    try:
        data = {'data':None,'error':False,'message':None}        
        if request.user.role == 'teacher' or request.user.role == 'student' or request.user.role == 'admin':                        
            VAPID_PUBLIC_KEY = django_settings.VAPID_PUBLIC_KEY
            data['VAPID_PUBLIC_KEY'] = VAPID_PUBLIC_KEY
            return JsonResponse(data,status=200)
        else:
            raise Exception("You're not allowed to perform this action")

    except Exception as e:
        print(e)
        data['message'] = str(e)
        data['error'] = True        
        return JsonResponse(data,status=500)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_web_push_subscription(request):
    try:
        data = {'data':None,'error':False,'message':None}
        body = request.data
        user_obj=None
        if request.user.role == 'teacher' or request.user.role == 'admin' or request.user.role == 'student':
            if request.user.role == 'teacher':
                user_obj = Teacher.objects.filter(profile=request.user).first()
            if request.user.role == 'admin':
                user_obj = Admin.objects.filter(profile=request.user).first()
            if request.user.role == 'student':
                user_obj = Student.objects.filter(profile=request.user).first()
            if user_obj:
                if 'subscription' in body and 'type' in body:
                    subscription_json = json.dumps(body['subscription'])
                    type = body.get('type')
                    notification_object,notification_object_created = NotificationSubscriptions.objects.get_or_create(subscription=subscription_json,subscription_type=type)
                    if notification_object_created:
                        user_obj.web_push_subscription.add(notification_object)
                        data['data'] = True
                        return JsonResponse(data,status=200)
                    else:
                        raise Exception("You've already subscribed")
                else:
                    raise Exception("Parameters Missing!!")    
            else:
                raise Exception("User does not exist")
        else:
            raise Exception("You're not allowed to perform this action")

    except Exception as e:
        print(e)
        data['message'] = str(e)
        data['error'] = True        
        return JsonResponse(data,status=500)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_branches_of_teacher(request):
    try:
        data = {'data':None,'error':False,'message':None}        
        if request.user.role == 'teacher':
            teacher_obj = Teacher.objects.filter(profile=request.user).first()
            if teacher_obj:
                branches = teacher_obj.branch_set.all()
                branches_serialized = BranchSerializer(branches,many=True)
                data['data'] = branches_serialized.data
                return JsonResponse(data,status=200)
            else:
                raise Exception("Teacher does not exist")
        else:
            raise Exception("You're not allowed to perform this action")

    except Exception as e:
        print(e)
        data['message'] = str(e)
        data['error'] = True        
        return JsonResponse(data,status=500)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_semesters_from_branch(request,branch_slug):
    try:
        data = {'data':None,'error':False,'message':None}        
        if request.user.role == 'teacher':
            teacher_obj = Teacher.objects.filter(profile=request.user).first()
            if teacher_obj:
                branch_obj = Branch.objects.filter(slug=branch_slug).first()
                if branch_obj:
                    streams = branch_obj.stream_set.all()
                    semesters = Semester.objects.filter(stream__in=streams)
                    semesters_serialized = SemesterSerializer(semesters,many=True)
                    data['data'] = semesters_serialized.data
                    return JsonResponse(data,status=200)
                else:
                    raise Exception('Branch does not exists')
            else:
                raise Exception("Teacher does not exist")
        else:
            raise Exception("You're not allowed to perform this action")

    except Exception as e:
        print(e)
        data['message'] = str(e)
        data['error'] = True        
        return JsonResponse(data,status=500)
    
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_divisons_from_semesters(request,semester_slug):
    try:
        data = {'data':None,'error':False,'message':None}        
        if request.user.role == 'teacher':
            teacher_obj = Teacher.objects.filter(profile=request.user).first()
            if teacher_obj:
                semester_obj = Semester.objects.filter(slug=semester_slug).first()
                if semester_obj:
                    divisions = Division.objects.filter(semester=semester_obj)
                    divison_serialized = DivisionSerializer(divisions,many=True)
                    data['data'] = divison_serialized.data
                    return JsonResponse(data,status=200)
                else:
                    raise Exception('Semester does not exists')
            else:
                raise Exception("Teacher does not exist")
        else:
            raise Exception("You're not allowed to perform this action")

    except Exception as e:
        print(e)
        data['message'] = str(e)
        data['error'] = True        
        return JsonResponse(data,status=500)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_batches_from_divison(request,divison_slug):
    try:
        data = {'data':None,'error':False,'message':None}        
        if request.user.role == 'teacher':
            teacher_obj = Teacher.objects.filter(profile=request.user).first()
            if teacher_obj:
                divison_obj = Division.objects.filter(slug=divison_slug).first()
                if divison_obj:
                    batches = Batch.objects.filter(division = divison_obj)
                    batch_serialized = BatchSerializer(batches,many=True)
                    data['data'] = batch_serialized.data
                    return JsonResponse(data,status=200)
                else:
                    raise Exception('Divison does not exists')
            else:
                raise Exception("Teacher does not exist")
        else:
            raise Exception("You're not allowed to perform this action")

    except Exception as e:
        print(e)
        data['message'] = str(e)
        data['error'] = True        
        return JsonResponse(data,status=500)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_batches_from_semester(request,semester_slug):
    try:
        data = {'data':None,'error':False,'message':None}        
        if request.user.role == 'admin':
            admin_obj = Admin.objects.filter(profile=request.user).first()
            if admin_obj:
                semester_obj = Semester.objects.filter(slug=semester_slug).first()
                if semester_obj:
                    batches = Batch.objects.filter(division__semester=semester_obj)
                    batch_serialized = BatchSerializer(batches,many=True)
                    data['data'] = batch_serialized.data
                    return JsonResponse(data,status=200)
                else:
                    raise Exception('Semester does not exists')
            else:
                raise Exception("Admin does not exist")
        else:
            raise Exception("You're not allowed to perform this action")

    except Exception as e:
        print(e)
        data['message'] = str(e)
        data['error'] = True        
        return JsonResponse(data,status=500)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_batches_from_subject(request,subject_slug):
    try:
        data = {'data':None,'error':False,'message':None}        
        if request.user.role == 'admin':
            admin_obj = Admin.objects.filter(profile=request.user).first()
            if admin_obj:
                subject_obj = Subject.objects.filter(slug=subject_slug).first()
                if subject_obj:
                    batches = subject_obj.included_batches.all()
                    batch_serialized = BatchSerializer(batches,many=True)
                    data['data'] = batch_serialized.data
                    return JsonResponse(data,status=200)
                else:
                    raise Exception('Subject does not exists')
            else:
                raise Exception("Admin does not exist")
        else:
            raise Exception("You're not allowed to perform this action")

    except Exception as e:
        print(e)
        data['message'] = str(e)
        data['error'] = True        
        return JsonResponse(data,status=500)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_subjects_of_student(request):
    try:
        data = {'data':None,'error':False,'message':None}
        if request.user.role == 'student':
            student_obj = Student.objects.filter(profile=request.user).first()
            if student_obj:
                subjects = Subject.objects.filter(included_batches__students = student_obj).distinct()
                subjects_serialized = SubjectSerializer(subjects,many=True)
                data['data'] = subjects_serialized.data
                return JsonResponse(data,status=200)
            else:
                raise Exception("Student does not exist")
        else:
            raise Exception("You're not allowed to perform this action")

    except Exception as e:
        print(e)
        data['message'] = str(e)
        data['error'] = True        
        return JsonResponse(data,status=500)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_master_timetable(request):
    try:
        data = {'logs':[],'register_count':0,'error_count':0,'error':False,'message':None}
        if request.user.role == 'admin':
            body = request.data
            admin_obj = Admin.objects.get(profile=request.user)
            branch_obj = admin_obj.branch_set.first()               
            if 'master_tt.csv' in body:
                df = pd.read_csv(body['master_tt.csv'])
                header_rows = df.iloc[:3].reset_index(drop=True)
                df.columns = df.iloc[3]
                df = df[4:].reset_index(drop=True) 
                faculties = list(df.columns[2:])
                # Check the format of the faculties row                
                for day, day_data in df.groupby('DAY'):                    
                    data['logs'].append(f"Schedule for {day}:")
                    rows = list(day_data.iterrows())
                    i = 0
                    while i < len(rows):
                        index, row = rows[i]        
                        for faculty in faculties:   
                            lecture_type = 'theory'
                            time_info = parse_time_string(row['TIME'])
                            if time_info:
                                info = parse_be_me_string(row[faculty]) if pd.notna(row[faculty]) else None                
                                if pd.notna(row[faculty]):
                                    current_lecture_hash = hash_string(row[faculty])
                                    # Also check if next consecutive lecture is not the same as current
                                    if i < len(rows) - 1: 
                                        next_row = rows[i+1][1]
                                        next_time_info = parse_time_string(next_row['TIME'])
                                        next_info = parse_be_me_string(next_row[faculty]) if pd.notna(next_row[faculty]) else None
                                        if pd.notna(next_row[faculty]):
                                            next_lecture_hash = hash_string(next_row[faculty])
                                            if next_lecture_hash == current_lecture_hash:
                                                time_info['end_time'] = next_time_info['end_time']
                                                rows[i+1][1][faculty] = None          
                                                lecture_type = 'lab'
                                if info:                    
                                    # Initialize the requirements dictionary object
                                    teacher_obj = Teacher.objects.filter(teacher_code=faculty).first()
                                    if not teacher_obj:
                                        data['logs'].append(f"Faculty not found at {row}")
                                        raise Exception('Faculty not found')
                                
                                    classroom_obj = branch_obj.classroom_set.filter(class_name=info['classroom']).first()
                                    if not classroom_obj:
                                        data['logs'].append(f"Classroom not found at {row}")
                                        raise Exception('Classroom not found')
                                    
                                    requirements = {
                                        'stream':info['stream'],
                                        'teacher':teacher_obj,
                                        'classroom':classroom_obj,
                                        'schedule':None,
                                        'time_info':time_info,
                                        'type':lecture_type,
                                        'subject':None,
                                        'batches':None
                                    }                                                                                
                                    # Get the stream object
                                    stream_obj = branch_obj.stream_set.filter(title=info['stream']).first()
                                    if not stream_obj:
                                        data['logs'].append(f"Stream not found at {row}")
                                        raise Exception('Stream not found')
                                    # Get the semester                        
                                    semester_obj = stream_obj.semester_set.filter(no=info['sem']).first()
                                    if not semester_obj:
                                        data['logs'].append(f"Semester not found at {row}")
                                        raise Exception('Semester not found')
                                    # Get the subject
                                    requirements['subject'] = semester_obj.subject_set.filter(short_name=info['sub']).first()
                                    # get the division
                                    # For ME there will be only 1 division per semester
                                    if info['stream'] == 'ME':
                                        division_obj = semester_obj.division_set.first()
                                        if not division_obj:
                                            data['logs'].append(f"Division not found at {row}")
                                            raise Exception('Division not found')
                                        # Now get the timetable object of this division
                                        timetable_object = division_obj.timetable_set.first()
                                        if not timetable_object:
                                            data['logs'].append(f"Timetable not found at {row}")
                                            raise Exception('Timetable not found')
                                        # Get the schedule Object of current day
                                        requirements['schedule'] = timetable_object.schedule_set.filter(day=day).first()
                                        if not requirements['schedule']:
                                            data['logs'].append(f"Schedule not found for day {day} at {row}")
                                            raise Exception(f"Schedule not found for day {day} at {row}")
                                        #  Get the first batch object of the division
                                        division_batches = division_obj.batch_set.all()
                                        if not division_batches:
                                            data['logs'].append(f"No batch found in the division at {row}")
                                            raise Exception(f"No batch found in the division at {row}")
                                        #  check if the batch is included in the subject list or not                                
                                        allowed_batches = check_for_batch_includance(requirements['subject'],division_batches)
                                        if not allowed_batches:
                                            data['logs'].append(f"No batches are allowed in the subject at {row}")
                                            raise Exception(f"No batches are allowed in the subject at {row}")
                                        requirements['batches'] = allowed_batches
                                    elif info['stream'] == 'BE':
                                        division_obj = semester_obj.division_set.filter(division_name=info['div']).first()
                                        if not division_obj:
                                            data['logs'].append(f"Division not found for at {row}")
                                            raise Exception(f'Division not found for at {row}')
                                        
                                        # Now get the timetable object of this division
                                        timetable_object = division_obj.timetable_set.first()
                                        if not timetable_object:
                                            data['logs'].append(f"Timetable not found for division at {row}")
                                            raise Exception(f'Timetable not found for division at {row}')

                                        # Get the schedule Object of current day
                                        requirements['schedule'] = timetable_object.schedule_set.filter(day=day).first()
                                        if not requirements['schedule']:
                                            data['logs'].append(f"Schedule not found for day {day} at {row}")
                                            raise Exception(f"Schedule not found for day {day} at {row}")

                                        # Get the batch
                                        if info['batch']:
                                            # Now we can get the batch
                                            requirements['batches'] = division_obj.batch_set.filter(batch_name=info['batch'])
                                            if not requirements['batches']:
                                                data['logs'].append(f"Batch not found with name at {row}")
                                                raise Exception(f"Batch not found with name at {row}")
                                        else:
                                            division_batches = division_obj.batch_set.all()
                                            if not division_batches:
                                                data['logs'].append(f"No batches found in the division at {row}")
                                                raise Exception(f"No batches found in the division at {row}")

                                            # Check if the batches are included in the subject list or not
                                            allowed_batches = check_for_batch_includance(requirements['subject'], division_batches)
                                            if not allowed_batches:
                                                data['logs'].append(f"No batches are allowed in the subject at {row}")
                                                raise Exception(f"No batches are allowed in the subject at {row}")
                                            
                                            requirements['batches'] = allowed_batches

                                    else:
                                        data['logs'].append(f"Unidentified stream found at {row}")
                                        raise Exception('Unidentified stream found')
                                    # Now we can add the lectures
                                    lecture_obj,created = Lecture.objects.get_or_create(start_time=requirements['time_info']['start_time'],end_time=requirements['time_info']['end_time'],schedule=requirements['schedule'],subject=requirements['subject'])
                                    if created:
                                        lecture_obj.type=requirements['type']                                
                                        lecture_obj.teacher=requirements['teacher']
                                        lecture_obj.classroom=requirements['classroom']
                                        lecture_obj.save()                                
                                        lecture_obj.batches.add(*requirements['batches'])
                                        # Need to create lecture sessions for this particular lecture...after that the cronjob will take care of it
                                        today = datetime.datetime.now().date()                    
                                        if lecture_obj:
                                            batches = lecture_obj.batches.all()
                                            lecture_session,created = Session.objects.get_or_create(lecture=lecture_obj,day=today,active='pre')
                                            if created:             
                                                students = Student.objects.filter(batch__in=batches)
                                                for student in students:
                                                    attendance_obj = Attendance.objects.create(student=student)
                                                    lecture_session.attendances.add(attendance_obj)
                                            data['logs'].append(f'Lecture added at {row[faculty]}')
                                        else:
                                            data['logs'].append(f"Lecture does not exists at {row}")
                                            raise Exception('Lecture does not exists')                                
                                    else:
                                        data['logs'].append(f"Lecture already exists for this timeslot {row}")                                        
                        i += 1                                
                            
                return JsonResponse(data,status=200)
            else:
                raise Exception('Parameters missing')
        else:
            raise Exception("You're not allowed to perform this action")
    except Exception as e:
        print(e)
        data['message'] = str(e)
        data['error'] = True        
        return JsonResponse(data,status=500)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_streams(request):
    try:
        data = {'data':None,'error':False,'message':None}        
        if request.user.role == 'admin':
            admin_obj = Admin.objects.filter(profile=request.user).first()
            if not admin_obj:raise Exception("Admin does not exists")
            branches = admin_obj.branch_set.all()
            if not branches.exists():raise Exception("No active branches currently!!")
            streams = Stream.objects.filter(branch__in=branches)
            if not streams:raise Exception("No streams found")
            streams_serialized = StreamSerializer(streams,many=True)
            data['data'] = streams_serialized.data
            return JsonResponse(data,status=200)
        elif request.user.role == 'teacher':
            teacher_obj = Teacher.objects.filter(profile=request.user).first()
            if not teacher_obj:raise Exception("Teacher does not exists")
            branches = teacher_obj.branch_set.all()
            if not branches.exists():raise Exception("Branch does not exists")
            streams = Stream.objects.filter(branch__in=branches)
            if not streams.exists():raise Exception("No streams found")
            streams_serialized = StreamSerializer(streams,many=True)
            data['data'] = streams_serialized.data
            return JsonResponse(data,status=200)
        else:
            raise Exception("You're not allowed to perform this action")

    except Exception as e:
        print(e)
        data['message'] = str(e)
        data['error'] = True        
        return JsonResponse(data,status=500)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_divisions_from_stream(request,stream_slug):
    try:
        data = {'data':None,'error':False,'message':None}        
        if request.user.role != 'admin':raise Exception("You're not allowed to perform this action")
        admin_obj = Admin.objects.filter(profile=request.user).first()
        if not admin_obj:raise Exception("Admin does not exists")
        stream_obj = Stream.objects.filter(slug=stream_slug).first()
        if not stream_obj: raise Exception("Stream does not exists")
        semesters = Semester.objects.filter(stream=stream_obj)
        if not semesters:raise Exception("No semester found")
        divisions = Division.objects.filter(semester__in=semesters)
        if not divisions:raise Exception("No division found")
        divisions_serialized = DivisionSerializer(divisions,many=True)
        data['data'] = divisions_serialized.data
        return JsonResponse(data,status=200)        
    except Exception as e:
        print(e)
        data['message'] = str(e)
        data['error'] = True        
        return JsonResponse(data,status=500)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_subjects_to_semester(request):
    try:
        data = {'data':None,'error':False,'message':None}
        if request.user.role != 'admin':raise Exception("You're not allowed to perform this action.")
        body = request.data
        if 'subject_slugs' not in body or 'semester_slug' not in body or 'deadline_timestamp' not in body:raise Exception("Parameters missing")
        deadline_timestamp_obj = datetime.datetime.fromtimestamp(int(body['deadline_timestamp'])).date()
        if deadline_timestamp_obj <=  datetime.date.today():raise Exception("The deadline date should be in the future.")
        semester_obj = Semester.objects.get(slug=body['semester_slug'])
        branch_obj = semester_obj.stream.branch
        if semester_obj.subjects_locked: raise Exception("Subjects are locked for this semester")
        permanent_subjects = PermanentSubject.objects.filter(slug__in=body['subject_slugs'])
        if not permanent_subjects.exists():raise Exception('No subjects chosen')
        # get the students and teachers profiles for later use        
        student_profiles = [student.profile for student in semester_obj.students.all()]
        teacher_profiles = [teacher.profile for teacher in branch_obj.teachers.all()]
        # We have to check if subject choices for this semester was already marked sometime before
        # All subjects from semester
        sem_subjects_set = semester_obj.subject_set.all()
        if sem_subjects_set.exists():        
            # check if any subject is removed from the previous subject set
            for subject_obj in sem_subjects_set:
                if subject_obj.subject_map not in permanent_subjects:                       
                    # for teacher
                    for teacher_profile in teacher_profiles:
                        subject_choice_obj = SubjectChoices.objects.get(profile=teacher_profile,semester=semester_obj)                        
                        subject_choice_obj.choices_locked=False
                        subject_choice_obj.save()
                    complementry_obj = subject_obj.complementrysubjects_set.first()
                    if complementry_obj:
                        complementry_obj_subjects = complementry_obj.subjects.exclude(id=subject_obj.id)
                        if complementry_obj_subjects.count() == 1:
                            for student_profile in student_profiles:
                                subject_choice_obj = SubjectChoices.objects.get(profile=student_profile,semester=semester_obj)
                                complementry_sub_to_removed_sub = complementry_obj_subjects.first()
                                complementry_sub_to_removed_sub.is_elective=False
                                complementry_sub_to_removed_sub.save()
                                subject_choice_obj.available_choices.remove(complementry_sub_to_removed_sub)
                                subject_choice_obj.finalized_choices.add(complementry_sub_to_removed_sub,through_defaults={'ordering': 1})
                            subject_obj.complementrysubjects_set.first().delete()
                        else:
                            for student_profile in student_profiles:
                                subject_choice_obj = SubjectChoices.objects.get(profile=student_profile,semester=semester_obj)
                                subject_choice_obj.available_choices.add(*complementry_obj_subjects)
                                subject_choice_obj.finalized_choices.remove(*complementry_obj_subjects)
                                subject_choice_obj.choices_locked=False
                                subject_choice_obj.save()
                    subject_obj.delete()
            semester_obj.subjects_locked=True
            semester_obj.subject_choice_deadline=deadline_timestamp_obj
            semester_obj.save()
            subjects_serialized = PermanentSubjectSerializer([subject for subject in permanent_subjects],many=True)
            data['data'] = subjects_serialized.data
            return JsonResponse(data,status=200)
        else:
            created_subjects = []
            while permanent_subjects.exists():
                permanent_subject = permanent_subjects.first()            
                # Check if the category matches with another subject in the list
                if permanent_subject.is_elective:   
                    # create complementry subjects here
                    complementries = permanent_subjects.filter(category=permanent_subject.category).exclude(id=permanent_subject.id)
                    if complementries.exists():
                        current_subject_obj,current_subject_created = Subject.objects.get_or_create(semester=semester_obj,subject_map=permanent_subject,is_elective=True)
                        complementry_obj,complementry_obj_created = ComplementrySubjects.objects.get_or_create(semester=semester_obj,category=permanent_subject.category)
                        complementry_obj.subjects.add(current_subject_obj)
                        for complimentry_subj in complementries:
                            subject_obj,subject_created = Subject.objects.get_or_create(semester=semester_obj,subject_map=complimentry_subj,is_elective=True)
                            created_subjects.append(subject_obj)
                            complementry_obj.subjects.add(subject_obj)
                            permanent_subjects = permanent_subjects.exclude(id=complimentry_subj.id)
                    else:
                        # Elective with no complementry                    
                        subject_obj,subject_created = Subject.objects.get_or_create(semester=semester_obj,subject_map=permanent_subject)                    
                        created_subjects.append(subject_obj)
                        permanent_subjects = permanent_subjects.exclude(id=permanent_subject.id)

                else:                
                    permanent_subjects = permanent_subjects.exclude(id=permanent_subject.id)
                    subject_obj,subject_created = Subject.objects.get_or_create(semester=semester_obj,subject_map=permanent_subject)
                    created_subjects.append(subject_obj)                    
            # Now to make the SubjectChoices objects
            # For teachers
            teacher_subject_choices_objects = []
            for teacher_profile in teacher_profiles:
                teacher_subject_choices_object = SubjectChoices.objects.filter(profile=teacher_profile,semester=semester_obj).first()
                if teacher_subject_choices_object:
                    teacher_subject_choices_object.available_choices.add(*created_subjects)
                else:
                    teacher_subject_choices_objects.append(SubjectChoices(profile=teacher_profile,semester=semester_obj,slug=generate_unique_hash()))
            # Now to bulk create the choices object and add the subjects it it
            SubjectChoices.objects.bulk_create(teacher_subject_choices_objects)
            for teacher_subject_choices_object in teacher_subject_choices_objects:
                teacher_subject_choices_object.available_choices.add(*created_subjects)
            # For students
            students_subject_choices_objects = []
            for student_profile in student_profiles:
                student_subject_choices_object = SubjectChoices.objects.filter(profile=student_profile,semester=semester_obj).first()
                if student_subject_choices_object:
                    electives = list(filter(lambda subject:subject.is_elective,created_subjects))
                    student_subject_choices_object.available_choices.add(*electives)
                else:
                    student_subject_choices_object = SubjectChoices(profile=student_profile,semester=semester_obj,slug=generate_unique_hash())
                    students_subject_choices_objects.append(student_subject_choices_object)
            # Now to bulk create the choices object and add the subjects it it
            SubjectChoices.objects.bulk_create(students_subject_choices_objects)
            electives = list(filter(lambda subject:subject.is_elective,created_subjects))
            for subject_choices_object in students_subject_choices_objects:
                subject_choices_object.available_choices.add(*electives)
            # Set the semester deadline
            semester_obj.subjects_locked=True
            semester_obj.subject_choice_deadline=deadline_timestamp_obj
            semester_obj.save()
            subjects_serialized = PermanentSubjectSerializer([subject.subject_map for subject in created_subjects],many=True)
            data['data'] = subjects_serialized.data
        return JsonResponse(data,status=200)
    except Exception as e:
        print(e)
        data['message'] = str(e)
        data['error'] = True        
        return JsonResponse(data,status=500)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_semesters_from_stream(request,stream_slug):
    try:
        data = {'data':{},'error':False,'message':None}
        if request.user.role == 'admin':
            stream_obj = Stream.objects.filter(slug=stream_slug).first()
            if not stream_obj: raise Exception("Stream does not exists")
            semesters = Semester.objects.filter(stream=stream_obj)
            if not semesters:raise Exception("No semester found")
            global_json_path = os.path.join(django_settings.BASE_DIR, 'globals.json')
            with open(global_json_path,'r') as global_json:
                globals_data = json.load(global_json)
                years = globals_data[f'{stream_obj.title}_YEARS']
            semesters_serialized = SemesterSerializerByStream(instance=semesters,many=True,years_arr=years)
            data['data']= semesters_serialized.data        
            return JsonResponse(data,status=200)
        if request.user.role == 'teacher':
            stream_obj = Stream.objects.filter(slug=stream_slug).first()
            if not stream_obj: raise Exception("Stream does not exists")
            semesters = Semester.objects.filter(stream=stream_obj)
            if not semesters:raise Exception("No semester found")
            semesters_serialized = SemesterSerializer(semesters,many=True)
            data['data']= semesters_serialized.data        
            return JsonResponse(data,status=200)

    except Exception as e:
        print(e)
        data['message'] = str(e)
        data['error'] = True
        return JsonResponse(data,status=500)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_semesters_only_from_stream(request,stream_slug):
    try:
        data = {'data':{},'error':False,'message':None}
        if request.user.role != 'admin': raise Exception("You're not allowed to perform this action!!")
        stream_obj = Stream.objects.filter(slug=stream_slug).first()
        if not stream_obj: raise Exception("Stream does not exists")
        semesters = Semester.objects.filter(stream=stream_obj)
        if not semesters:raise Exception("No semester found")                    
        semesters_serialized = SemesterOnlySerializerByStream(instance=semesters,many=True)
        data['data']= semesters_serialized.data        
        return JsonResponse(data,status=200)
    except Exception as e:
        print(e)
        data['message'] = str(e)
        data['error'] = True
        return JsonResponse(data,status=500)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_subjects_from_acedemic_year(request,semester_slug,acedemic_year):
    try:
        data = {'data':{},'error':False,'message':None}
        if request.user.role != 'admin':raise Exception("You're not allowed to perform this action")
        admin_obj = Admin.objects.filter(profile=request.user).first()
        if not admin_obj:raise Exception("Admin does not exists")
        semester_obj = Semester.objects.filter(slug=semester_slug).first()
        if not semester_obj: raise Exception("Semester does not exists")
        permanent_subject_objs = PermanentSubject.objects.filter(degree=semester_obj.stream.title,stream_code=semester_obj.stream.stream_code,sem_year=semester_obj.no,acedemic_year=acedemic_year)
        if not permanent_subject_objs:raise Exception("No Subject found!!")
        permanent_subject_serialized = PermanentSubjectSerializer(permanent_subject_objs,many=True)
        data['data'] = permanent_subject_serialized.data
        return JsonResponse(data,status=200)
    except Exception as e:
        print(e)
        data['message'] = str(e)
        data['error'] = True
        return JsonResponse(data,status=500)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_teachers_subject_choices(request,semester_slug):
    try:
        data = {'data':{},'error':False,'message':None}
        if request.user.role != 'teacher':raise Exception("You're not allowed to perform this action")
        semester= Semester.objects.get(slug=semester_slug)
        subject_choices_object = SubjectChoices.objects.filter(profile=request.user,semester=semester).first()
        if not subject_choices_object: raise Exception("No Subject Choices found for this teacher")
        # Check if the choices are locked or not        
        if subject_choices_object.choices_locked:            
            finalized_subjects_set = subject_choices_object.finalized_choices.order_by('orderedfinalizedsubject__ordering')
            subject_choices_object_serialized = PermanentSubjectSerializer(instance = [subject.subject_map for subject in finalized_subjects_set],many=True)
            data['data']['finalized_choices'] = subject_choices_object_serialized.data
        else:
            available_subjects_set = subject_choices_object.available_choices.all()
            subject_choices_object_serialized = PermanentSubjectSerializer(instance = [subject.subject_map for subject in available_subjects_set],many=True)
            data['data']['available_choices'] = subject_choices_object_serialized.data
        data['data']['choices_locked'] = subject_choices_object.choices_locked
        data['data']['deadline_timestamp']=semester.subject_choice_deadline
        data['data']['slug']=subject_choices_object.slug    
        return JsonResponse(data,status=200)
    except Exception as e:
        print(e)
        data['message'] = str(e)
        data['error'] = True
        return JsonResponse(data,status=500)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_students_subject_choices(request):
    try:
        data = {'data':{},'error':False,'message':None}
        if request.user.role != 'student':raise Exception("You're not allowed to perform this action")
        student_obj = Student.objects.get(profile=request.user)
        term_obj = Term.objects.filter(status=True).first()
        if not term_obj: raise Exception("No active term found for now")
        students_semester = Semester.objects.filter(stream__branch__term=term_obj,students=student_obj).first()
        if not students_semester: raise Exception("No semester found for current term for now")
        subject_choices_object = SubjectChoices.objects.filter(profile=request.user,semester=students_semester).first()
        if not subject_choices_object: raise Exception("No Subject Choices found for this Student")
        if subject_choices_object.choices_locked:
            finalized_subjects_set = subject_choices_object.finalized_choices.order_by('orderedfinalizedsubject__ordering')
            finalized_subject_choices_object_serialized = PermanentSubjectSerializer(instance = [subject.subject_map for subject in finalized_subjects_set],many=True)
            data['data']['finalized_choices'] = finalized_subject_choices_object_serialized.data            
        else:
            available_subjects_set = subject_choices_object.available_choices.all()
            available_complementry_subject_objs = set(ComplementrySubjects.objects.filter(subjects=subject).first() for subject in available_subjects_set)
            available_subject_choices_object_serialized = ComplementrySubjectsSerializer(instance = available_complementry_subject_objs,many=True,available_subjects=available_subjects_set)
            data['data']['available_choices'] = available_subject_choices_object_serialized.data        
        data['data']['choices_locked'] = subject_choices_object.choices_locked
        data['data']['deadline_timestamp']=students_semester.subject_choice_deadline
        data['data']['slug']=subject_choices_object.slug
        return JsonResponse(data,status=200)
    except Exception as e:
        print(e)
        data['message'] = str(e)
        data['error'] = True
        return JsonResponse(data,status=500)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_subject_choices(request):
    try:
        data = {'data':{},'error':False,'message':None}                
        if request.user.role != 'teacher' and request.user.role != 'student':raise Exception("You're not allowed to perform this action.")        
        body = request.data
        if 'subject_choices' not in body or 'subject_choices_slug' not in body:raise Exception("Parameters missing")        
        subject_choices_obj = SubjectChoices.objects.get(slug=body['subject_choices_slug'])        
        semester_obj = subject_choices_obj.semester
        if not subject_choices_obj:raise Exception("No Subject Choices were found at this moment.")                
        if subject_choices_obj.profile != request.user: raise Exception("You're not allowed to fill this choice")                        
        if subject_choices_obj.choices_locked: raise Exception("Your choice has been already locked")
        finalized_permanent_subjects = sorted(PermanentSubject.objects.filter(slug__in=body['subject_choices']).prefetch_related('subject_set'),key=lambda subject: body['subject_choices'].index(subject.slug))
        if len(finalized_permanent_subjects) == 0: raise Exception("No choices given")
        finalized_subjects = [permanent_subject.subject_set.first() for permanent_subject in finalized_permanent_subjects]
        if request.user.role=='student':            
            complementry_subjects = ComplementrySubjects.objects.filter(
                    semester=semester_obj,
                    id__in=subject_choices_obj.available_choices.values_list('id', flat=True)
            )            
            # Check atleast one of all complementry choices has been marked by the user
            for complementry_subjects_obj in complementry_subjects:
                elective_choice_found = False
                for elective_sub in complementry_subjects_obj.subjects.all():
                    if elective_sub in finalized_subjects:
                        elective_choice_found=True
                if not elective_choice_found:                    
                    raise Exception("Please choose from all the elective categories")  
        for order, subject in enumerate(finalized_subjects, start=(subject_choices_obj.finalized_choices.count() + 1)):
            # Check for student to only add one of the complementry subject (Not possible for frontend but just in case)
            # Logic will be just chcek the subject in the complement subject object's subjects field if the subject beside this one is already in the finalized_subjects queryset field then don't allow to add this one or replace the current
            # we can't let the student add choice of a pemanent subject
            # Also have to check the user only tries to add choice for the subject which is in his available sujects list
            if not subject_choices_obj.available_choices.contains(subject):                
                # for teacher and student both
                continue
            if request.user.role=='student':
                # only for student
                if not subject.is_elective:                    
                    continue
                complementries = ComplementrySubjects.objects.filter(subjects=subject).first().subjects.exclude(id=subject.id)
                with transaction.atomic():
                    for complementry in complementries:
                        if complementry in finalized_subjects:
                            subject_choices_obj.finalized_choices.clear()
                            raise Exception("You can mark add choice for only 1 subject from the electives")
                        subject_choices_obj.available_choices.remove(complementry)
            subject_choices_obj.finalized_choices.add(subject, through_defaults={'ordering': order})
            subject_choices_obj.available_choices.remove(subject)

                
        subject_choices_obj.choices_locked=True
        subject_choices_obj.save()        
        finalized_subjects_set = subject_choices_obj.finalized_choices.order_by('orderedfinalizedsubject__ordering')
        subject_choices_object_serialized = PermanentSubjectSerializer(instance = [subject.subject_map for subject in finalized_subjects_set],many=True)
        data['data']['finalized_choices'] = subject_choices_object_serialized.data
        data['data']['choices_locked'] = subject_choices_obj.choices_locked
        data['data']['deadline_timestamp']=semester_obj.subject_choice_deadline
        data['data']['slug']=subject_choices_obj.slug
        return JsonResponse(data,status=200)
    except Exception as e:
        print(e)
        data['message'] = str(e)
        data['error'] = True
        return JsonResponse(data,status=500)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_teachers_for_the_subject(request,subject_slug):
    try:
        data = {'data':{},'error':False,'message':None}        
        if request.user.role != 'admin':raise Exception("You're not allowed to perform this action.")        
        subject_obj = Subject.objects.filter(subject_map__slug=subject_slug).first()
        if not subject_obj: raise Exception("Subject does not exists")
        # get the subject choies objects
        subject_choices_objs = SubjectChoices.objects.filter(profile__role='teacher',finalized_choices=subject_obj,choices_locked=True).prefetch_related(
            'finalized_choices', 'profile'
        )
        if not subject_choices_objs.exists(): raise Exception("No Choices for this subject")        
        subject_choices_objs_serialized = FinalizedSubjectChoicesSerializer(instance=subject_choices_objs,subject=subject_obj,many=True)
        data['data'] = subject_choices_objs_serialized.data
        return JsonResponse(data,status=200)
    except Exception as e:
        print(e)
        data['message'] = str(e)
        data['error'] = True
        return JsonResponse(data,status=500)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_complementry_subject_from_semester(request,semester_slug):
    try:
        data = {'data':[],'error':False,'message':None}
        if request.user.role != 'admin':raise Exception("You're not allowed to perform this action")                
        semester_obj = Semester.objects.filter(slug=semester_slug).first()
        if not semester_obj: raise Exception("Semester does not exists")
        complementry_subjects = ComplementrySubjects.objects.filter(semester=semester_obj).prefetch_related('subjects')
        if not complementry_subjects: raise Exception("No elective subject ofund for this semester")        
        complementry_subjects_serialized = ComplementrySubjectsSerializer(instance = complementry_subjects,many=True)        
        data['data'] = complementry_subjects_serialized.data
        return JsonResponse(data,status=200)
    except Exception as e:
        print(e)
        data['message'] = str(e)
        data['error'] = True
        return JsonResponse(data,status=500)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_students_for_the_subject(request,subject_slug):
    try:
        data = {'data':{},'error':False,'message':None}
        if request.user.role != 'admin':raise Exception("You're not allowed to perform this action")
        subject_obj = Subject.objects.filter(subject_map__slug=subject_slug).first()
        if not subject_obj:raise Exception("Subject does not exists")
        subject_choices_objs = SubjectChoices.objects.filter(profile__role='student',finalized_choices=subject_obj)
        if not subject_choices_objs.exists(): raise Exception("No student choices for this subject")
        subject_choices_objs_serialized = FinalizedSubjectChoicesSerializer(instance=subject_choices_objs,subject=subject_obj,many=True)
        data['data'] = subject_choices_objs_serialized.data
        return JsonResponse(data,status=200)
    except Exception as e:
        print(e)
        data['message'] = str(e)
        data['error'] = True
        return JsonResponse(data,status=500)
        
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unlock_subject_choices(request):
    try:
        data = {'data':None,'error':False,'message':None}
        if request.user.role != 'admin':raise Exception("You're not allowed to perform this action.")
        body = request.data
        if 'semester_slug' not in body:raise Exception("parameters missing!!")
        semester_obj = Semester.objects.get(slug=body['semester_slug'])
        if not semester_obj.subjects_locked:raise Exception("Choice already unlocked")
        semester_obj.subjects_locked=False
        semester_obj.save()
        data['data']=True
        return JsonResponse(data,status=200)
    except Exception as e:
        print(e)
        data['message'] = str(e)
        data['error'] = True
        return JsonResponse(data,status=500)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_subject_choice_groups(request,semester_slug):
    try:        
        data = {'data':{},'error':False,'message':None}
        if request.user.role != 'admin':raise Exception("You're not allowed to perform this action.")
        semester_obj = Semester.objects.get(slug=semester_slug)
        if semester_obj.subject_choice_deadline >  datetime.date.today() or not semester_obj.subjects_locked:raise Exception("The subject choice deadline for this semester has not been reached yet!!")
        # Check if the divisions are created or not
        divisions = Division.objects.filter(semester=semester_obj)
        if divisions.exists():
            divisions_cached = cache.get(f"divisions_{semester_obj.slug}")
            if divisions_cached:            
                data['data']['divisions'] = divisions_cached
                return JsonResponse(data,status=200)
            divisions_arr = []
            for division in divisions:
                batches = Batch.objects.filter(division=division)
                if batches.exists():                    
                    division_obj = {}
                    division_obj["division_name"]= division.division_name
                    division_obj['total_batches'] = []
                    division_obj['batches'] = []
                    total_students = set()
                    for batch in batches:
                        students = batch.students.all()
                        division_obj['total_batches'].append(batch.batch_name)
                        students_serialized = StudentSerializer(students,many=True)
                        total_students.update(students)
                        division_obj['batches'].append({'batch_name':batch.batch_name,'student_count':students.count(),'students':students_serialized.data})                
                    division_obj['total_student_count'] = len(total_students)
                divisions_arr.append(division_obj)
            data['data']['divisions'] = divisions_arr
            cache.set(f"divisions_{semester_obj.slug}", divisions_arr, timeout=3600)
            return JsonResponse(data,status=200)
        subject_groups = SubjectGroups.objects.filter(semester=semester_obj)
        if subject_groups.exists():
            subject_groups_serialized = SubjectGroupSerializer(subject_groups,many=True)
            data['data'] = subject_groups_serialized.data
        else:
            subject_groups = {}
            student_subject_choices = SubjectChoices.objects.filter(semester=semester_obj, profile__role='student').order_by('profile__student__enrollment')
            if not student_subject_choices.exists():raise("No choices for this semester")
            for subject_choice_obj in student_subject_choices:
                student = subject_choice_obj.profile.student_set.first()
                subject_group = subject_choice_obj.finalized_choices.all()
                subject_group_tuple = tuple(subject_group)
                if subject_group_tuple not in subject_groups:
                    subject_groups[subject_group_tuple] = [student]
                else:
                    subject_groups[subject_group_tuple].append(student)

            # Storing the subject gruops
            subject_groups_objs = []
            for subjects,students in subject_groups.items():
                subject_groups = SubjectGroups.objects.filter(semester=semester_obj,subjects__in=subjects)                
                subject_group_obj = SubjectGroups.objects.create(semester=semester_obj)
                subject_group_obj.subjects.add(*subjects)
                subject_group_obj.students.add(*students)
                subject_groups_objs.append(subject_group_obj)
            subject_groups_serialized = SubjectGroupSerializer(subject_groups_objs,many=True)
            data['data'] = subject_groups_serialized.data
        return JsonResponse(data,status=200)
    except Exception as e:
        print(e)
        data['message'] = str(e)
        data['error'] = True
        return JsonResponse(data,status=500)
      
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_division_suggestion(request,semester_slug):
    try:        
        data = {'data':{},'error':False,'message':None}
        if request.user.role != 'admin':raise Exception("You're not allowed to perform this action.")
        semester_obj = Semester.objects.get(slug=semester_slug)
        body = request.query_params
        if 'max_students' not in body:raise Exception("Pleae send a maximum student size count for the division")
        division_suggestion_dict = cache.get(f'division_suggestion_{semester_obj.slug}_{body["max_students"]}')
        if division_suggestion_dict:            
            data['data'] = division_suggestion_dict
            return JsonResponse(data,status=200)
        subject_groups_qs = SubjectGroups.objects.filter(semester=semester_obj)
        subject_groups =  {}        
        total_hours = {}
        for subject_group in subject_groups_qs:
            subjects = frozenset(subject_group.subjects.all())
            subject_groups[subjects] = subject_group.students.all()            
            for subject in subjects:
                if subject not in total_hours:
                    total_hours[subject] = subject.subject_map.L + subject.subject_map.T + subject.subject_map.P
        # Constraints
        min_students = 0  # No minimum size for divisions
        max_students = int(body['max_students'])  # Maximum size per division
        result, subject_hours = allocate_groups_with_splitting(subject_groups, total_hours, min_students, max_students)
        hour_deviations = []
        for subject, hours in subject_hours.items():
            deviation = {
                "subject_name":subject.subject_map.subject_name,
                "initial_hours":total_hours[subject],
                "final_hours":hours                    
                }
            hour_deviations.append(deviation)
        divisions = []
        if result["divisions"]:
            for i, division in enumerate(result["divisions"]):
                division_name=string.ascii_uppercase[i]
                division_obj = {}
                division_obj["division_name"]=division_name
                subject_to_student_map = {division_name: set()}  # Initialize with 'common' key
                student_count_for_division = sum(len(students) for _, students in division)
                division_obj['total_student_count'] = student_count_for_division
                for group, students in division:
                    student_set = set(students)
                    subject_to_student_map[division_name].update(student_set)  # Add students to 'common'

                    if len(division) != 1:
                        for subject in group:
                            if subject.is_elective:
                                subject_to_student_map.setdefault(subject, set()).update(student_set)                
                # Now we can make batches        
                division_obj['total_batches'] = []
                division_obj['batches'] = []
                # make common batches for the divisions
                common_students = set()
                # if subject is elective them made serpate batches
                for subject,students in subject_to_student_map.items():            
                    if  type(subject)!=str and not subject.is_elective:
                        common_students.update(set(students))     
                        continue          
                    batches = create_batches(subject,students)
                    for batch in batches:
                        division_obj['total_batches'].append(batch)
                        students_serialized = StudentSerializer(batches[batch],many=True)
                        division_obj['batches'].append({'batch_name':batch,'student_count':len(batches[batch]),'students':students_serialized.data})
                divisions.append(division_obj)
        data['data']['divisions'] = divisions
        data['data']['hour_deviations']=hour_deviations
        cache.set(f"division_suggestion_{semester_obj.slug}_{max_students}", data['data'], timeout=3600)
        return JsonResponse(data,status=200)
    except Exception as e:
        print(e)
        data['message'] = str(e)
        data['error'] = True
        return JsonResponse(data,status=500)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unlock_subject_choice_for_student(request):
    try:
        data = {'data':{},'error':False,'message':None}
        if request.user.role != 'admin':raise Exception("You're not allowed to perform this action.")
        body = request.data
        if 'subject_choices_slug' not in body and 'subject_slug' not in body: raise Exception("Parameters missing!!")
        subject_obj = Subject.objects.get(subject_map__slug=body["subject_slug"])
        subject_choice_obj = SubjectChoices.objects.get(slug=body['subject_choices_slug'])
        if not subject_choice_obj.finalized_choices.contains(subject_obj):
            raise Exception(f"Student has not selected {subject_obj.subject_map.subject_name}")
        complementry_obj = subject_obj.complementrysubjects_set.first()
        complementry_obj_subjects = complementry_obj.subjects.exclude(id=subject_obj.id)
        if complementry_obj_subjects.count() == 1:
            complementry_sub_to_add = complementry_obj_subjects.first()
            subject_choice_obj.finalized_choices.add(complementry_sub_to_add,through_defaults={'ordering': 1})
            subject_choices_object_serialized = PermanentSubjectSerializer(instance = complementry_sub_to_add.subject_map)
            data['data']['subject']=subject_choices_object_serialized.data
        else:   
            subject_choice_obj.available_choices.add(*complementry_obj_subjects)
            subject_choice_obj.choices_locked = False
            subject_choice_obj.save()
            data['data']['subject']= None
        subject_choice_obj.finalized_choices.remove(subject_obj)
        data['data']['choice_locked'] = subject_choice_obj.choices_locked
        data['data']["subject_delete"] = True
        return JsonResponse(data,status=200)
    except Exception as e:
        print(e)
        data['message'] = str(e)
        data['error'] = True
        return JsonResponse(data,status=500)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def confirm_suggested_divisions(request):
    try:
        data = {'data':None,'error':False,'message':None}
        if request.user.role != 'admin':raise Exception("You're not allowed to perform this action.")
        body = request.data        
        if 'divisions_data' not in body and 'semester_slug' not in body: raise Exception("Parameters missing!!")
        semester_obj = Semester.objects.get(slug=body['semester_slug'])
        for division_data in body['divisions_data']['divisions']:            
            division_obj,division_created = Division.objects.get_or_create(division_name=division_data['division_name'],semester=semester_obj)
            if division_created:            
                for batch_data in division_data['batches']:
                    batch_obj,batch_created = Batch.objects.get_or_create(batch_name=batch_data['batch_name'],division=division_obj)
                    if batch_created:
                        student_slugs = [student['slug'] for student in batch_data['students']]                        
                        students = Student.objects.filter(slug__in=student_slugs)
                        batch_obj.students.add(*students)
        data['data']=True
        return JsonResponse(data,status=200)
    except Exception as e:
        print(e)        
        data['message'] = str(e)
        data['error'] = True
        return JsonResponse(data,status=500)
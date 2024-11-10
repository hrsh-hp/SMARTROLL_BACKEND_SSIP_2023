from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from django.http import JsonResponse
from Manage.models import Division, Semester,Batch,TimeTable,Schedule,Classroom,Lecture,Term,Link,Stream,PermanentSubject,Semester,Subject,Branch,College,Term,Stream,ComplementrySubjects
from StakeHolders.models import Admin,Teacher,Student,NotificationSubscriptions,SuperAdmin
from Profile.models import Profile
from .serializers import SemesterSerializer,DivisionSerializer,BatchSerializer,SubjectSerializer,TimeTableSerializer,ClassRoomSerializer,LectureSerializer,TermSerializer,TimeTableSerializerForTeacher,TimeTableSerializerForStudent,LectureSerializerForHistory,BranchWiseTimeTableSerializer,BranchWiseTimeTableSerializerStudent,BranchSerializer,StreamSerializer,PermanentSubjectSerializer
from Session.models import Session,Attendance
import pandas as pd
from django.contrib.auth import get_user_model
from StakeHolders.serializers import TeacherSerializer
import datetime
from django.conf import settings as django_settings
import os
from django.core.mail import send_mail
from threading import Thread
from .utils import parse_be_me_string,parse_time_string,hash_string,check_for_batch_includance
import json
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
        print(request.user.role)
        if request.user.role == 'admin':
            admin_obj = Admin.objects.filter(profile=request.user).first()
            if not admin_obj:raise Exception("Admin does not exists")
            branch_obj = admin_obj.branch_set.first()
            if not branch_obj:raise Exception("Branch does not exists")
            streams = branch_obj.stream_set.all()
            if not streams:raise Exception("No streams found")
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
        if 'subject_slugs' not in body or 'semester_slug' not in body:raise Exception("Parameters missing")
        semester_obj = Semester.objects.get(slug=body['semester_slug'])
        permanent_subjects = PermanentSubject.objects.filter(slug__in=body['subject_slugs'])        
        created_subjects = []
        while permanent_subjects.exists():
            permanent_subject = permanent_subjects.first()            
            # Check if the category matches with another subject in the list
            if permanent_subject.is_elective:   
                # create complementry subjects here
                complementries = permanent_subjects.filter(category=permanent_subject.category)
                if complementries.count() == 1 and complementries.first() == permanent_subject:                    
                    permanent_subjects = permanent_subjects.exclude(id=permanent_subject.id)
                    subject_obj,subject_created = Subject.objects.get_or_create(semester=semester_obj,subject_map=permanent_subject)
                    created_subjects.append(subject_obj.subject_map)
                    permanent_subjects = permanent_subjects.exclude(id=permanent_subject.id)
                    continue
                complementry_obj,complementry_created = ComplementrySubjects.objects.get_or_create(semester=semester_obj)
                for complimentry_subj in complementries:
                    subject_obj,subject_created = Subject.objects.get_or_create(semester=semester_obj,subject_map=complimentry_subj)
                    created_subjects.append(subject_obj.subject_map)
                    complementry_obj.subjects.add(subject_obj)
                    permanent_subjects = permanent_subjects.exclude(id=complimentry_subj.id)
            else:                
                permanent_subjects = permanent_subjects.exclude(id=permanent_subject.id)
                subject_obj,subject_created = Subject.objects.get_or_create(semester=semester_obj,subject_map=permanent_subject)
                created_subjects.append(subject_obj.subject_map)
        subjects_serialized = PermanentSubjectSerializer(created_subjects,many=True)
        data['data'] = subjects_serialized.data
        return JsonResponse(data,status=200)
    except Exception as e:
        print(e)
        data['message'] = str(e)
        data['error'] = True        
        return JsonResponse(data,status=500)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_semsters_from_stream(request,stream_slug):
    try:
        data = {'data':{},'error':False,'message':None}
        if request.user.role != 'admin':raise Exception("You're not allowed to perform this action")
        admin_obj = Admin.objects.filter(profile=request.user).first()
        if not admin_obj:raise Exception("Admin does not exists")
        stream_obj = Stream.objects.filter(slug=stream_slug).first()
        if not stream_obj: raise Exception("Stream does not exists")
        semesters = Semester.objects.filter(stream=stream_obj)
        if not semesters:raise Exception("No semester found")
        semesters_serialized = SemesterSerializer(semesters,many=True)
        global_json_path = os.path.join(django_settings.BASE_DIR, 'globals.json')
        with open(global_json_path,'r') as global_json:
            globals_data = json.load(global_json)
            years = globals_data[f'{stream_obj.title}_YEARS']
        data['data']['semesters'] = semesters_serialized.data
        data['data']['years'] = years
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
        if not semester_slug: raise Exception("Semester does not exists")
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
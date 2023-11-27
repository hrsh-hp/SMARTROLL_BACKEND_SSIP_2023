from django.shortcuts import render
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from django.http import JsonResponse
from Manage.models import Semester,Branch,Subject
from .models import Timetable,Schedule,Lecture,Classroom
from .serializers import TimetableSerializer,ClassRoomSerializer,LectureSerializer
from django.db import transaction
from StakeHolders.models import Admin,Teacher
from StakeHolders.serializers import TeacherProfileSerializer
from Manage.serializers import SubjectSerializer
import pandas as pd
import random
from datetime import time

# Create your views here.

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_timetable(request):
    try:
        if request.user.role == 'admin' or request.user.role == 'teacher':
            body = request.GET
            if 'semester_slug' not in body:
                raise Exception('Please provide a valid semester slug')
            semester_obj = Semester.objects.get(slug=body.get('semester_slug'))            
            if semester_obj:
                # Make the time table
                time_table = semester_obj.time_table.all().first()
                if time_table:                    
                    time_table_serialized = TimetableSerializer(time_table)
                    data = {"timetable":time_table_serialized.data}
                else:
                    with transaction.atomic():
                        # We have to make a new timetable
                        time_table_obj = Timetable()
                        time_table_obj.save()  # Save the Timetable instance
                        # Make 7 new schedule objects
                        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
                        for i in days:
                            schedule_obj = Schedule(day=i)
                            schedule_obj.save()
                            time_table_obj.schedules.add(schedule_obj)
                            time_deltas = [(time(hour=10,minute=30,second=0),time(hour=11,minute=30,second=0)),(time(hour=11,minute=30,second=0),time(hour=12,minute=30,second=0)),(time(hour=13,minute=0,second=0),time(hour=14,minute=0,second=0)),(time(hour=14,minute=0,second=0),time(hour=15,minute=0,second=0)),(time(hour=15,minute=15,second=0),time(hour=16,minute=15,second=0)),(time(hour=16,minute=15,second=0),time(hour=17,minute=15,second=0))]
                            for j in time_deltas:                      
                                lecture_obj = Lecture(start_time = j[0],end_time = j[1])                                
                                lecture_obj.save()  # Save the Lecture instance
                                schedule_obj.lectures.add(lecture_obj)
                        semester_obj.time_table.add(time_table_obj)
                    time_table_serialized = TimetableSerializer(time_table_obj)
                    data = {"timetable":time_table_serialized.data}
                return JsonResponse(data,status=200)
        else:
            data = {"data":"You're not allowed to perform this action"}
            return JsonResponse(data,status=401)
    except Exception as e:
        print(e)
        data = {"data":str(e)}
        return JsonResponse(data,status=500)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def handle_excel_upload(request):
    if request.method == 'POST' and request.FILES['excel_data']:
        try:
            excel_file = request.FILES['excel_data']
            df = pd.read_excel(excel_file)            

            # Now you have the DataFrame 'df', and you can perform further processing.

            response_data = {'message': 'Excel file uploaded and processed successfully.'}
            return JsonResponse(response_data, status=200)
        except Exception as e:
            response_data = {'error': str(e)}
            return JsonResponse(response_data, status=500)

    else:
        response_data = {'error': 'Invalid request method or no file provided.'}
        return JsonResponse(response_data, status=400)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_objects_for_lecture(request):
    '''
    ### Get Objects for Lecture

    #### Endpoint:

    - **Method:** GET
    - **URL:** `/api/get_objects_for_lecture/`

    #### Authentication:

    - Requires authentication with a valid token.

    #### Permissions:

    - Requires the user to have the 'admin' role.

    #### Parameters:

    - `semester_slug` (string, required): The slug of the semester for which objects are requested.

    #### Response:

    ```json
    {
        "subjects": [
            {
                "slug": "169719_1700459626",
                "subject_name": "Analysis And Design Of Algorithms",
                "code": 3150703,
                "credit": 5,
                "teachers": [
                    {
                        "id": 5,
                        "profile": {
                            "name": "Shraddha Modi",
                            "email": "shraddhamodi@gmail.com",
                            "ph_no": "9925717005"
                        }
                    },
                    {
                        "id": 3,
                        "profile": {
                            "name": "kishan nurani",
                            "email": "kishan@gmail.com",
                            "ph_no": "919925717005"
                        }
                    }
                ]
            },
            {
                "slug": "317463_1700459688",
                "subject_name": "Professional Ethics",
                "code": 3150709,
                "credit": 3,
                "teachers": [
                    {
                        "id": 1,
                        "profile": {
                            "name": "Pragnesh Patel",
                            "email": "pragneshpatel@gmail.com",
                            "ph_no": "919925717005"
                        }
                    }
                ]
            },
            {
                "slug": "276506_1700459713",
                "subject_name": "Computer Networks",
                "code": 3150710,
                "credit": 5,
                "teachers": [
                    {
                        "id": 3,
                        "profile": {
                            "name": "kishan nurani",
                            "email": "kishan@gmail.com",
                            "ph_no": "919925717005"
                        }
                    }
                ]
            },
            {
                "slug": "465827_1700459730",
                "subject_name": "Software Engineering",
                "code": 3150711,
                "credit": 5,
                "teachers": [
                    {
                        "id": 2,
                        "profile": {
                            "name": "vimal vaghela",
                            "email": "vimalvaghela@gmail.com",
                            "ph_no": "7874032915"
                        }
                    }
                ]
            },
            {
                "slug": "318459_1700472974",
                "subject_name": "Python for Data Science",
                "code": 3150713,
                "credit": 3,
                "teachers": []
            },
            {
                "slug": "183385_1700473124",
                "subject_name": " Cyber Security",
                "code": 3150714,
                "credit": 2,
                "teachers": [
                    {
                        "id": 5,
                        "profile": {
                            "name": "Shraddha Modi",
                            "email": "shraddhamodi@gmail.com",
                            "ph_no": "9925717005"
                        }
                    }
                ]
            }
        ],
        "classrooms": [
            {
                "slug": "492036_1700305422",
                "class_name": "CE_101"
            },
            {
                "slug": "215962_1700305439",
                "class_name": "CE_102"
            },
            {
                "slug": "103216_1700305454",
                "class_name": "CE_103"
            },
            {
                "slug": "179211_1700305529",
                "class_name": "CE_104"
            },
            {
                "slug": "219981_1700305543",
                "class_name": "CE_105"
            },
            {
                "slug": "752835_1700305558",
                "class_name": "CE_106"
            },
            {
                "slug": "117893_1700305579",
                "class_name": "CE_107"
            },
            {
                "slug": "247468_1700305592",
                "class_name": "CE_108"
            },
            {
                "slug": "428503_1700305639",
                "class_name": "CE_109"
            },
            {
                "slug": "968839_1700305653",
                "class_name": "CE_110"
            }
        ]
    }
    ```

    #### Status Codes:

    - 200 OK: Successfully retrieved objects.
    - 401 Unauthorized: User does not have the required role.
    - 500 Internal Server Error: An error occurred on the server.
    '''
    try:
        if request.user.role == 'admin' or request.user.role == 'teacher':
            if request.user.role == 'teacher':
                teacher_obj = Teacher.objects.get(profile=request.user)
                admin_obj = teacher_obj.branch.admin_set.first()
            else:                
                admin_obj = Admin.objects.get(profile=request.user)
            branch_obj = admin_obj.branch
            body = request.GET
            if 'semester_slug' not in body:
                raise Exception('Please provide valid semester slug')
            semester_obj = Semester.objects.get(slug=body['semester_slug'])
            subjects_obj = semester_obj.subjects.all()
            subjects = []
            for i in subjects_obj:
                subject_obj = SubjectSerializer(i)
                subject_obj_serialized = subject_obj.data
                teachers_obj = TeacherProfileSerializer(i.teacher_set.all(),many=True)
                subject_obj_serialized['teachers'] = teachers_obj.data
                subjects.append(subject_obj_serialized)            
            classrooms = Classroom.objects.filter(branch=branch_obj).all()
            classrooms_serialized = ClassRoomSerializer(classrooms,many=True)            
            data = {
                'subjects':subjects,
                'classrooms':classrooms_serialized.data,                
            }
            return JsonResponse(data,status=200)
        else:
            data = {"data":"You're not allowed to perform this action"}
            return JsonResponse(data,status=401)
    except Exception as e:
        data = {"data":str(e)}
        return JsonResponse(data,status=500)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def set_lecture_attributes(request):
    '''
    ### Set Lecture Attributes

    #### Endpoint:

    - **Method:** POST
    - **URL:** `/api/set_lecture_attributes/`

    #### Authentication:

    - Requires authentication with a valid token.

    #### Permissions:

    - Requires the user to have the 'admin' role.

    #### Parameters:

    - `lecture_slug` (string, required): The slug of the lecture for which attributes are to be set.
    - `teacher_id` (integer, required): The ID of the teacher to assign to the lecture.
    - `subject_slug` (string, required): The slug of the subject to assign to the lecture.
    - `classroom_slug` (string, required): The slug of the classroom to assign to the lecture.

    #### Response:

    ```json
    {
        "lecture": {
            "slug": "216906_1700490876",
            "teacher": 5,
            "subject": {
                "slug": "169719_1700459626",
                "subject_name": "Analysis And Design Of Algorithms",
                "code": 3150703,
                "credit": 5
            },
            "classroom": {
                "slug": "492036_1700305422",
                "class_name": "CE_101"
            },
            "start_time": "04:15 P.M.",
            "end_time": "05:15 P.M."
        }
    }
    ```

    #### Status Codes:

    - 200 OK: Lecture attributes set successfully.
    - 401 Unauthorized: User does not have the required role.
    - 500 Internal Server Error: An error occurred on the server.
    '''
    try:
        if request.user.role == 'admin' or request.user.role == 'teacher':
            body = request.data
            if 'lecture_slug' not in body:
                raise Exception('parameters Missing!')
            if 'teacher_id' not in body:
                raise Exception('parameters Missing!')
            if 'subject_slug' not in body:
                raise Exception('parameters Missing!')
            if 'classroom_slug' not in body:
                raise Exception('parameters Missing!')

            with transaction.atomic():
                lecture_obj = Lecture.objects.get(slug=body['lecture_slug'])
                subject_obj = Subject.objects.get(slug = body['subject_slug'])
                classroom_obj = Classroom.objects.get(slug=body['classroom_slug'])
                if 'proxy_id' in body:
                    proxy_obj = Teacher.objects.get(id=body['proxy_id'])
                    teacher_obj = Teacher.objects.get(id=body['teacher_id'])
                    lecture_obj.teacher = proxy_obj
                    lecture_obj.teacher_proxy = teacher_obj
                else:
                    teacher_obj = Teacher.objects.get(id=body['teacher_id'])
                    lecture_obj.teacher = teacher_obj
                lecture_obj.subject = subject_obj
                lecture_obj.classroom = classroom_obj
                lecture_obj.save()
            lecture_obj_serialized = LectureSerializer(lecture_obj)
            return JsonResponse(data={'lecture':lecture_obj_serialized.data},status=200)
        else:
            data = {"data":"You're not allowed to perform this action"}
            return JsonResponse(data,status=401)
    except Exception as e:
        data = {"data":str(e)}
        return JsonResponse(data,status=500)
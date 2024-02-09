from django.urls import path,include
from .views import get_object_counts,add_semester,get_semesters,add_division,add_batch,get_batches,get_divisions,add_teacher,get_teachers,get_subjects,add_subject,get_timetable,get_lecture_configs,add_lecture_to_schedule,upload_students_data
urlpatterns = [        
    path('get_object_counts',get_object_counts,name='get_object_counts'),    
    path('add_semester/',add_semester,name='add_semester'),
    path('get_semesters',get_semesters,name='get_semesters'),
    path('add_division/',add_division,name='add_division'),
    path('get_subject',get_subjects,name='get_subjects'),
    path('add_subject/',add_subject,name='add_subject'),
    path('add_batch/',add_batch,name='add_batch'),
    path('get_batches',get_batches,name='get_batches'),
    path('get_divisions',get_divisions,name='get_divisions'),
    path('add_teacher/',add_teacher,name='add_teacher'),
    path('get_teacher',get_teachers,name='get_teachers'),
    path('get_timetable',get_timetable,name='get_timetable'),
    path('get_lecture_configs',get_lecture_configs,name='get_lecture_configs'),
    path('add_lecture_to_schedule/',add_lecture_to_schedule,name='add_lecture_to_schedule'),
    path('upload_students_data/',upload_students_data,name='upload_students_data')
]

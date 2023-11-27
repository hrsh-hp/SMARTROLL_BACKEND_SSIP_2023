from django.urls import path
from .views import get_session_student,get_session_teacher

urlpatterns = [
    path('get_session_student',get_session_student),
    path('get_session_teacher',get_session_teacher),
]


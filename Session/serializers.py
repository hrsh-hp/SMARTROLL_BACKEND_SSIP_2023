from rest_framework import serializers
from .models import Session,Attendance
from StakeHolders.serializers import StudentSerializers

class AttendanceSerializer(serializers.ModelSerializer):
    student = StudentSerializers() 
    class Meta:
        model = Session
        fields = ['student','is_verified','physically_present']

class SessionSerializer(serializers.ModelSerializer):
    attendance = AttendanceSerializer(many=True)
    class Meta:
        model = Session
        fields = ['session_id','total_students','attendance','present_student_count','absent_student_count','status','created_at']
    
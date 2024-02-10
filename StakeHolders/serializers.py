from .models import Admin,Teacher,Student
from rest_framework import serializers
from Manage.serializers import BranchSerializer
from Profile.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['name','email','ph_no','role']


class AdminSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer() 
    branches = serializers.SerializerMethodField()
    class Meta:
        model = Admin
        fields = ['id','profile','branches']
    
    def get_branches(self,obj):
        branches = obj.branch_set.all()
        branches_serialized = BranchSerializer(branches,many=True)
        return branches_serialized.data

class TeacherSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()    
    branches = serializers.SerializerMethodField()

    class Meta:
        model = Teacher
        fields = ['slug','profile','branches']
    
    def get_branches(self,obj):
        branches = obj.branch_set.all()
        branches_serialized = BranchSerializer(branches,many=True)
        return branches_serialized.data
    
class StudentSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()    
    branches = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = ['slug','profile','branches']
    
    def get_branches(self,obj):
        branches = obj.branch_set.all()
        branches_serialized = BranchSerializer(branches,many=True)
        return branches_serialized.data
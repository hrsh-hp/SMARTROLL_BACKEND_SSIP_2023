from rest_framework.decorators import api_view
from django.http import JsonResponse
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
import base64
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
import json
import secrets
from django.conf import settings as django_settings
from StakeHolders.models import Student
from Profile.models import Profile
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render,redirect
from django.core.mail import send_mail
import uuid
import time
from threading import Thread

def send_password_to_email(to,password):
    message = f'Your Email is : {to}....And Password is {password}'
    send_mail(subject='Your credentials for SmartRoll',message=message, from_email= django_settings.EMAIL_HOST_USER,recipient_list=[to])

def generate_unique_hash():    
    random_hash = str(uuid.uuid4().int)[:6]    
    timestamp = str(int(time.time()))    
    unique_hash = f"{random_hash}_{timestamp}"
    return unique_hash

@api_view(['GET'])
def check_server_avaibility(request):
    return JsonResponse(data={'data':True},status=200)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_token_authenticity(request):
    return JsonResponse(data={'data':True},status=200)     

@csrf_exempt
def studet_registration_response(request):
    print(request.POST)
    response = {'error':False,"data":None,'message':None}
    try:
        if request.method == 'POST':
            if 'name' in request.POST and 'email' in request.POST and 'phone' in request.POST:            
                name = request.POST['name']
                email = request.POST['email']
                ph_no = request.POST['phone']
                password = generate_unique_hash()                
                profile_obj,created = Profile.objects.get_or_create(email=email,password=password)
                profile_obj.name = name
                profile_obj.ph_no = ph_no
                profile_obj.role = 'student'
                profile_obj.save()
                student_obj,created = Student.objects.get_or_create(profile=profile_obj)
                if(created):
                    Thread(target=send_password_to_email,args=(email,password)).start()
                    response['data'] = "You've been registered"
                else:
                    raise Exception("You've already been registered")
            else:
                raise Exception('Parameters missing')        
    except Exception as e:
        response['error'] = True
        response['message'] = str(e)

    return JsonResponse(response)
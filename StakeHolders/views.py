from django.shortcuts import render
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import (
    TokenObtainPairView,    
    TokenRefreshView,
)
from rest_framework.decorators import api_view
from .models import Admin,Student
from Profile.models import Profile
from .serializers import AdminSerializer,StudentSerializer
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from django.contrib.auth import authenticate

# Create your views here.

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def get_token(self, user):        
        token = super().get_token(user)        
        token['role'] = user.role
        token['email'] = user.email
        token['username'] = user.name
        token['is_actvie'] = user.name
        return token

@api_view(['POST'])   
def RegisterUser(request):
    body = request.data
    response = {'error':False,"data":None,'message':None}
    try:
        if 'name' in body and 'ph_no' in body and 'email' in body and 'password' in body:
            # Create a profile obj
            profile_obj,created = Profile.objects.get_or_create(email=body['email'],password=body['password'])
            profile_obj.name = body['name']
            profile_obj.ph_no = body['ph_no']
            profile_obj.role = 'student'
            profile_obj.save()            
            student_obj,created = Student.objects.get_or_create(profile=profile_obj)
            student_obj_serialized = StudentSerializer(student_obj)
            response['data'] = student_obj_serialized.data
        else:
            raise Exception('Parameters Missing')
    except Exception as e:
        response['error'] = True
        response['message'] = str(e)

    return JsonResponse(response)    



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_token_authenticity(request):
    '''
    ## Check Token Authenticity

    **Path:** `/auth/api/check_token_authenticity`

    **Method:** `GET`

    **Authorization:** Token-based (Authentication required)

    ### Description
    Check the authenticity of the authentication token.

    ### Permissions
    - Requires user to be authenticated.

    ### Response
    - **Status Code:** 200 OK
    - **Content:**
    ```json
    {
        "data": true
    }
    ```
    Indicates that the token is authentic.

    ### Error Response
    - **Status Code:** 401 Unauthorized
    ```json
    {
        "detail": "Authentication credentials were not provided."
    }
    ```
    Indicates that the request lacks proper authentication credentials.

    ---

    *Note: Make sure to include the authentication token in the request header when accessing this endpoint.*
    '''
    return JsonResponse({'data':True},status=200)

    
class CustomTokenObtainPairView(TokenObtainPairView):
    """    
    # Allowed Method - POST
    #### Input:
    - `param1`: email.
    - `param2`: password.

    #### Output:
    `if user exists`
    - access token, refresh token.    
    
    `if user does not exists`
    - Response status code will be another than 200.
    """    
    serializer_class = CustomTokenObtainPairSerializer    

class CustomTokenRefreshView(TokenRefreshView):
    """    
    # Allowed Method - POST
    #### Input:
    - `param1`: refresh token.    

    #### Output:
    - `If refresh token is valid `: new access token, new refresh token.
    - `If refresh token is not valid`: Response status code will be another than 200.
    """        

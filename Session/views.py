from django.shortcuts import render
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from django.http import JsonResponse
from StakeHolders.models import Student
from TimeTable.models import Lecture
from .serializers import SessionSerializer
from .models import Session

# Create your views here.

from django.shortcuts import get_object_or_404

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_session_student(request):
    '''
    # Get Session Student

        Retrieves information about an active session for a student.

        - **URL**: `/api/get-session-student/`

        - **Method**: `GET`

        - **Authentication Required**: Yes

        - **Permissions Required**: IsAuthenticated

        ## Request

        ### Query Parameters

        | Parameter      | Type   | Description                                |
        | -------------- | ------ | ------------------------------------------ |
        | `lecture_slug` | String | **Required.** Slug of the associated lecture. |

        ## Response

        ### Success Response

        - **Status Code**: `200 OK`

        ```json
        {
        "data": true,
        "session": {
            // Serialized session data
        }
        }
        ```

        ### Error Responses

        - **Status Code**: `401 Unauthorized`

        ```json
        {
        "data": "You're not allowed to perform this action"
        }
        ```

        - **Status Code**: `500 Internal Server Error`

        ```json
        {
        "data": "Error message"
        }
        ```

        ## Notes

        - The user must be authenticated and have the role of 'student' to access this endpoint.
        - If the lecture slug is not provided, a `400 Bad Request` response will be returned.
        - If the lecture or session is not found, a `404 Not Found` response will be returned.
        - If the session is not active, a `400 Bad Request` response will be returned.
        - In case of any other error, a `500 Internal Server Error` response will be returned.
        '''
    try:                
        print(request.user.role)
        if request.user.role != 'student':
            data = {"data": "You're not allowed to perform this action"}
            return JsonResponse(data, status=401)

        lecture_slug = request.query_params.get('lecture_slug')
        if not lecture_slug:
            raise Exception('Provide all the parameters')

        lecture_obj = get_object_or_404(Lecture, slug=lecture_slug)

        if not lecture_obj.session:
            raise Exception('Session is not active yet')

        session = lecture_obj.session
        session_serialized = SessionSerializer(session)
        data = {'data': True, 'session': session_serialized.data}
        return JsonResponse(data, status=200)
    except Exception as e:
        print(e)
        data = {"data": str(e)}
        return JsonResponse(data, status=500)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_session_teacher(request):
    '''
    # Get Session Teacher

    Creates or retrieves information about an active session for a teacher.

    - **URL**: `/api/get-session-teacher/`

    - **Method**: `POST`

    - **Authentication Required**: Yes

    - **Permissions Required**: IsAuthenticated

    ## Request

    ### Body Parameters

    | Parameter      | Type   | Description                                |
    | -------------- | ------ | ------------------------------------------ |
    | `lecture_slug` | String | **Required.** Slug of the associated lecture. |

    ## Response

    ### Success Response

    - **Status Code**: `200 OK`

    ```json
    
    "data": true,
    "session": {
        "session_id": "0072d577db4732b27bf5a1a4ac55d8073b5fc93730a896a3919ba3863c1fab4f",
        "total_students": [
            71,
            70,
            73
        ],
        "attendance": [],
        "present_student_count": null,
        "absent_student_count": null,
        "status": true
        }
    }
    ```

    ### Error Responses

    - **Status Code**: `401 Unauthorized`

    ```json
    {
    "data": "You're not allowed to perform this action"
    }
    ```

    - **Status Code**: `500 Internal Server Error`

    ```json
    {
    "data": "Error message"
    }
    ```

    ## Notes

    - The user must be authenticated and have the role of 'teacher' to access this endpoint.
    - If the lecture slug is not provided, a `400 Bad Request` response will be returned.
    - If the session already exists for the provided lecture, its information will be retrieved.
    - If the session is not active or has been disabled, a `400 Bad Request` response will be returned.
    - If the session is created successfully, its information will be returned in the response.
    '''
    try:         
        body = request.data            
        if request.user.role != 'teacher':
            data = {"data": "You're not allowed to perform this action"}
            return JsonResponse(data, status=401)

        if 'lecture_slug' not in body:
            raise Exception('Provide all the parameters')
        
        lecture_obj = get_object_or_404(Lecture, slug=body['lecture_slug'])

        # Check if session already exists
        if lecture_obj.session:
            session = lecture_obj.session
            if session.status:
                session_serialized = SessionSerializer(session)
                data = {'data': True, 'session': session_serialized.data}
                return JsonResponse(data, status=200)
            else:
                raise Exception('Session is not Active or has been disabled')
        
        # Create a session
        session = Session(status=True)
        session.save()
        lecture_obj.session  = session
        lecture_obj.save()
        session.total_students.set(session.lecture_set.first().subject.student_set.all())
        session_serialized = SessionSerializer(session)
        data = {'data': True, 'session': session_serialized.data}
        return JsonResponse(data, status=200)
    except Exception as e:
        print(e)
        data = {"data": str(e)}
        return JsonResponse(data, status=500)
 
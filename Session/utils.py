import requests
from StakeHolders.serializers import StudentSerializer

def notify_teacher_about_marking(student_obj,session_id):
    node_endpoint = "https://0f0f-2409-40c1-3012-24b3-8323-3b2f-677a-10da.ngrok-free.app/socket/manage/student_attendace_data"
    headers = {
        'ngrok-skip-browser-warning': 'true'  # Custom header
    }
    student_obj_serialized = StudentSerializer(student_obj)
    data = {
        'session_id':session_id,
        'student_data':student_obj_serialized.data
    }        
    response = requests.post(node_endpoint, headers=headers, data=data)
    return response
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Alert
from .serializers import AlertSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_alerts(request):
    data = {'data':None,'error':False,'message':None}    
    try:        
        alert_objs = Alert.objects.filter(profile=request.user)
        alert_objs_serialized = AlertSerializer(alert_objs,many=True)
        data['data'] = alert_objs_serialized.data
        return Response(data,status=200)
    except Exception as e:
        print(e)
        data['message'] = str(e)
        data['error'] = True     
        return Response(data,status=500) 

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_all_as_read(request):
    data = {'data':None,'error':False,'message':None}    
    try:        
        Alert.objects.filter(profile=request.user, status='unseen').update(status='seen')
        alert_objs = Alert.objects.filter(profile=request.user)
        alert_objs_serialized = AlertSerializer(alert_objs, many=True)
        data['data'] = alert_objs_serialized.data
        return Response(data,status=200)
    except Exception as e:
        print(e)
        data['message'] = str(e)
        data['error'] = True     
        return Response(data,status=500)   

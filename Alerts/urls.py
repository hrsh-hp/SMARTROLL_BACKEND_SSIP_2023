from django.urls import path
from .views import get_alerts
urlpatterns = [         
    path('get_alerts',get_alerts,name='get_alerts'),
]
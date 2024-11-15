from django.urls import path
from .views import get_alerts,mark_all_as_read
urlpatterns = [         
    path('get_alerts',get_alerts,name='get_alerts'),
    path('mark_all_as_read/',mark_all_as_read,name='get_alerts'),
]
from django.urls import path
from .views import CustomTokenObtainPairView,CustomTokenRefreshView,check_token_authenticity,student_register,forgot_password,set_new_password_for_stakeholders

urlpatterns = [
    path('api/set_new_password_for_stakeholders/', set_new_password_for_stakeholders, name='set_new_password_for_stakeholders'),
    path('api/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),    
    path('api/check_token_authenticity', check_token_authenticity, name='check_token_authenticity'),
    path('api/register/', student_register, name='student_register'),
    path('api/forgot_password/', forgot_password, name='forgot_password'),
]

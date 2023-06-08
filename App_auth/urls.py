from django.urls import path
from App_auth.views import CustomTokenObtainPairView, CustomTokenRefreshView, CreateUserView


app_name = 'App_auth'

urlpatterns = [
    path('user/create/', CreateUserView.as_view(), name="create-user"),
    path('login/', CustomTokenObtainPairView.as_view(), name="login-user"),
    path('login/refresh/', CustomTokenRefreshView.as_view(), name="token-refresh"),
]
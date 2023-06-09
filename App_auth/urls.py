from django.urls import path
from App_auth.views import CustomTokenObtainPairView, CustomTokenRefreshView, CreateUserView, AdminProfileViewSet, \
    ResearcherProfileViewSet, ReviewerProfileViewSet, ReaderProfileViewSet

app_name = 'App_auth'

urlpatterns = [
    path('user/create/', CreateUserView.as_view(), name="create-user"),
    path('login/', CustomTokenObtainPairView.as_view(), name="login-user"),
    path('login/refresh/', CustomTokenRefreshView.as_view(), name="token-refresh"),
    path('admin-profiles/', AdminProfileViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('admin-profiles/<int:pk>/',
         AdminProfileViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('researcher-profiles/', ResearcherProfileViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('researcher-profiles/<int:pk>/',
         ResearcherProfileViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('reviewer-profiles/', ReviewerProfileViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('reviewer-profiles/<int:pk>/',
         ReviewerProfileViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('reader-profiles/', ReaderProfileViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('reader-profiles/<int:pk>/',
         ReaderProfileViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
]

from django.urls import path
from App_main.views import *


app_name = 'App_main'

urlpatterns = [
    path('researchpapers/', ResearchPaperViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('researchpapers/<int:pk>/',
         ResearchPaperViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),

]
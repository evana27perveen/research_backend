from django.urls import path
from App_main.views import *


app_name = 'App_main'

urlpatterns = [
    path('research-papers/', ResearchPaperViewSet.as_view({'get': 'list', 'post': 'create'})),

]
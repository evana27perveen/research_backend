from django.urls import path
from App_main.views import *


app_name = 'App_main'

urlpatterns = [
    path('researchpapers/', ResearchPaperViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('researchpapers/<int:pk>/',
         ResearchPaperViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('author-info/<int:pk>/', AuthorInfo.as_view(), name='author-info'),
    path('user-home-data/', UserHomeData.as_view(), name='user-home-data'),
    path('research-data/', LatestResearchPapersAPIView.as_view(), name='research-data'),
    path('research-papers/', ResearchPapersAPIView.as_view(), name='research-papers'),
    path('my-research-data/', MyResearchPapersAPIView.as_view(), name='my-research-data'),
    path('add-comment/', CommentViewSet.as_view({'get': 'list', 'post': 'create'}), name='add-comment'),
    path('comment-count/<int:pk>/', CommentCountAPIView.as_view(), name='comment-count'),
    path('comments/<int:pk>/', CommentsAPIView.as_view(), name='comments'),
    path('check-plagiarism/', CheckPlagiarismView.as_view(), name='check_plagiarism'),
]

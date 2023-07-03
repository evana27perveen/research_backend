from django.urls import path
from App_main.views import *


app_name = 'App_main'

urlpatterns = [
    path('researchpapers/', ResearchPaperViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('researchpapers/<int:pk>/',
         ResearchPaperViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('researchpapers/<int:pk>/mark_as_reviewed/', ResearchPaperViewSet.as_view({'put': 'mark_as_reviewed'})),
    path('researchpapers/<int:pk>/mark_as_pending/', ResearchPaperViewSet.as_view({'put': 'mark_as_pending'})),
    path('researchpapers/<int:pk>/mark_as_publish/', ResearchPaperViewSet.as_view({'put': 'mark_as_publish'})),
    path('author-info/<int:pk>/', AuthorInfo.as_view(), name='author-info'),
    path('user-home-data/', UserHomeData.as_view(), name='user-home-data'),
    path('research-data/', LatestResearchPapersAPIView.as_view(), name='research-data'),
    path('research-papers/', ResearchPapersAPIView.as_view(), name='research-papers'),
    path('all-research-papers/', AllResearchPapersAPIView.as_view(), name='all-research-papers'),
    path('my-research-data/', MyResearchPapersAPIView.as_view(), name='my-research-data'),
    path('review-research-data/', ReviewResearchPapersAPIView.as_view(), name='review-research-data'),
    path('publish-research-data/', PublishResearchPapersAPIView.as_view(), name='publish-research-data'),
    path('add-comment/', CommentViewSet.as_view({'get': 'list', 'post': 'create'}), name='add-comment'),
    path('comment-count/<int:pk>/', CommentCountAPIView.as_view(), name='comment-count'),
    path('comments/<int:pk>/', CommentsAPIView.as_view(), name='comments'),
    path('check-plagiarism/', CheckPlagiarismView.as_view(), name='check_plagiarism'),
]

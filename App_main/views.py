from rest_framework.response import Response

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView

from App_auth.serializers import ResearcherProfileModelSerializer
from App_main.plagiarism_checker import check_single_paper
from App_main.serializers import *
from rest_framework.permissions import BasePermission


class IsResearcher(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='RESEARCHER').exists()


class IsReader(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='READER').exists()


class IsReviewer(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='REVIEWER').exists()


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='ADMIN').exists()


class UserHomeData(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        profile_exists_or_not = False
        user = request.user
        user_groups = user.groups.all()
        group_names = [group.name for group in user_groups]
        if group_names[0] == 'ADMIN':
            profile_exists_or_not = AdminProfileModel.objects.filter(user=user).exists()
        elif group_names[0] == 'RESEARCHER':
            profile_exists_or_not = ResearcherProfileModel.objects.filter(user=user).exists()
        elif group_names[0] == 'REVIEWER':
            profile_exists_or_not = ReviewerProfileModel.objects.filter(user=user).exists()
        elif group_names[0] == 'READER':
            profile_exists_or_not = ReaderProfileModel.objects.filter(user=user).exists()

        return Response({"profile": f"{profile_exists_or_not}"})


class UnauthenticatedReadPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action == 'list':
            return True
        return request.user and request.user.is_authenticated


class ResearchPaperViewSet(viewsets.ModelViewSet):
    queryset = ResearchPaperModel.objects.all()
    serializer_class = ResearchPaperSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data["author"] = self.request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=False, methods=['GET'])
    def custom_action(self, request):
        return Response("Custom Action")

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = CommentModel.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class LatestResearchPapersAPIView(APIView):
    def get(self, request):
        latest_papers = ResearchPaperModel.objects.filter(status='published').order_by('-publication_date')[:9]
        serializer = ResearchPaperSerializer(latest_papers, many=True)
        return Response({"research_papers": serializer.data})


class ResearchPapersAPIView(APIView):
    def get(self, request):
        latest_papers = ResearchPaperModel.objects.filter(status='published').order_by('-publication_date')
        serializer = ResearchPaperSerializer(latest_papers, many=True)
        return Response({"research_papers": serializer.data})


class MyResearchPapersAPIView(APIView):
    permission_classes = [IsAuthenticated, IsResearcher]

    def get(self, request):
        user = request.user
        research_papers = ResearchPaperModel.objects.filter(author=user)
        serializer = ResearchPaperSerializer(research_papers, many=True)
        return Response({"research_papers": serializer.data})


class AuthorInfo(APIView):
    def get(self, request, pk):
        profile = get_object_or_404(ResearcherProfileModel, user=pk)
        serializer = ResearcherProfileModelSerializer(profile)
        return Response(serializer.data)


class CommentCountAPIView(APIView):
    def get(self, request, pk):
        comments = CommentModel.objects.filter(research_paper=pk).count()
        return Response({"comments": comments})


from rest_framework.generics import get_object_or_404


class CommentsAPIView(APIView):
    def get(self, request, pk):
        research_paper = get_object_or_404(ResearchPaperModel, pk=pk)
        comments = research_paper.comments.all()
        serializer = CommentSerializer(comments, many=True)

        research_paper_serializer = ResearchPaperSerializer(research_paper)
        data = {
            'research_paper': research_paper_serializer.data,
            'comments': serializer.data
        }

        return Response(data)


class CheckPlagiarismView(APIView):
    def post(self, request, *args, **kwargs):
        input_paper_file = request.FILES.get('file')
        
        if input_paper_file:
            check_result = check_single_paper(input_paper_file)
            data = {
                'score': check_result*100,
            }

            return Response(data)
        else:
            return Response({'error': 'No file provided.'}, status=400)


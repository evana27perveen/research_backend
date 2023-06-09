from rest_framework.response import Response

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import user_passes_test
from App_auth.models import *
from App_main.models import *
from App_main.serializers import *


def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()


def is_researcher(user):
    return user.groups.filter(name='RESEARCHER').exists()


def is_reviewer(user):
    return user.groups.filter(name='REVIEWER').exists()


def is_reader(user):
    return user.groups.filter(name='READER').exists()


class ResearchPaperViewSet(viewsets.ModelViewSet):
    queryset = ResearchPaperModel.objects.all()
    serializer_class = ResearchPaperSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    @user_passes_test(is_researcher)
    def create(self, request, **kwargs):
        serializer = self.serializer_class(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        research_paper = serializer.save(authors=[request.user])
        return Response({"status": "Successfully Created"}, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk, **kwargs):
        research_paper = ResearchPaperModel.objects.get(pk=pk)
        serializer = self.serializer_class(research_paper)
        return Response(serializer.data)

    def update(self, request, pk, **kwargs):
        research_paper = ResearchPaperModel.objects.get(pk=pk)
        serializer = self.serializer_class(research_paper, data=request.data, partial=True,
                                           context={"request": request})
        serializer.is_valid(raise_exception=True)
        research_paper = serializer.save()
        return Response({"status": "Successfully Updated!"})

    @user_passes_test(is_researcher)
    def destroy(self, request, pk, **kwargs):
        research_paper = ResearchPaperModel.objects.get(pk=pk)
        research_paper.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = CommentModel.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)



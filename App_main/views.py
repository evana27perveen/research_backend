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


def apply_decorator_to_methods(decorator):
    def decorator_wrapper(cls):
        for attr in cls.__dict__:
            if callable(getattr(cls, attr)):
                setattr(cls, attr, decorator(getattr(cls, attr)))
        return cls
    return decorator_wrapper


class ResearchPaperViewSet(viewsets.ModelViewSet):
    queryset = ResearchPaperModel.objects.all()
    serializer_class = ResearchPaperSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    @user_passes_test(is_researcher)
    def publish(self, request, pk=None):
        research_paper = self.get_object()
        if not research_paper.published:
            research_paper.published = True
            research_paper.save()
            return Response({"status": "Research paper published."}, status=status.HTTP_200_OK)
        return Response({"status": "Research paper already published."}, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(authors=[self.request.user])

    def perform_update(self, serializer):
        serializer.save(authors=[self.request.user])


class CommentViewSet(viewsets.ModelViewSet):
    queryset = CommentModel.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
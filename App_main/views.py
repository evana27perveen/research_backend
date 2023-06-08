from rest_framework import viewsets, permissions, generics
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.views import APIView
from django.contrib.auth.decorators import login_required, user_passes_test
from rest_framework.permissions import IsAuthenticated

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


@apply_decorator_to_methods(user_passes_test(is_researcher))
class ResearchPaperViewSet(viewsets.ModelViewSet):
    queryset = ResearchPaper.objects.all()
    serializer_class = ResearchPaperSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(authors=[self.request.user])

    def perform_update(self, serializer):
        serializer.save(authors=[self.request.user])


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
from rest_framework.response import Response

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import user_passes_test
from rest_framework.views import APIView

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
        latest_papers = ResearchPaperModel.objects.order_by('-publication_date')[:9]
        serializer = ResearchPaperSerializer(latest_papers, many=True)
        return Response(serializer.data)

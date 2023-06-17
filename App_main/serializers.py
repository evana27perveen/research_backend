from rest_framework import serializers
from App_main.models import ResearchPaperModel, CommentModel
from App_auth.models import *


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    class Meta:
        model = CommentModel
        fields = '__all__'


class ResearchPaperSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResearchPaperModel
        fields = ('id', 'author', 'title', 'Topic', 'file', 'citation', 'publication_date', 'status')
        read_only_fields = ('id', 'publication_date')



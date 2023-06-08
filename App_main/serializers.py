from rest_framework import serializers
from App_main.models import ResearchPaperModel, CommentModel


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    class Meta:
        model = CommentModel
        fields = '__all__'


class ResearchPaperSerializer(serializers.ModelSerializer):
    authors = serializers.StringRelatedField(many=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = ResearchPaperModel
        fields = '__all__'

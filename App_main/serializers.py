from rest_framework import serializers
from App_main.models import ResearchPaper, Comment


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    class Meta:
        model = Comment
        fields = '__all__'


class ResearchPaperSerializer(serializers.ModelSerializer):
    authors = serializers.StringRelatedField(many=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = ResearchPaper
        fields = '__all__'

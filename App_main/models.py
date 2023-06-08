from django.db import models
from App_auth.models import *


class ResearchPaper(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('rejected', 'Rejected'),
        ('accepted', 'Accepted'),
    )

    title = models.CharField(max_length=255)
    authors = models.ManyToManyField('ProfileModel')
    abstract = models.TextField()
    publication_date = models.DateField()
    file = models.FileField(upload_to='research_papers/')
    published = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.title} - ({self.status})"


class Comment(models.Model):
    research_paper = models.ForeignKey(ResearchPaper, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.research_paper.title}"

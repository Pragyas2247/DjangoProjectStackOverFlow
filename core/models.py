from django.contrib.auth.models import AbstractUser
from django.db import models

class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class User(AbstractUser):
    reputation = models.IntegerField(default=0)

class Question(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()  #Question
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    body = models.TextField()  #Answer
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    is_accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Vote(models.Model):
    VOTE_TYPE = (
        ('up', 'Upvote'),
        ('down', 'Downvote'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, null=True, blank=True, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, null=True, blank=True, on_delete=models.CASCADE)
    vote_type = models.CharField(choices=VOTE_TYPE, max_length=10)


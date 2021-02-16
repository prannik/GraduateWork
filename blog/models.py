from django.db import models
from django.utils import timezone


class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=48)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    counter = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.title}'


class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, blank=True, null=True)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, blank=True, null=True)
    text = models.TextField(max_length=300)
    date = models.DateTimeField(auto_now_add=True)
    counter = models.IntegerField(default=0)


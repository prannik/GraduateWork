from django.db import models
from django import forms


class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=48)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    counter = models.IntegerField(default=0)
    post_likes = models.IntegerField(default=0)
    post_dislikes = models.IntegerField(default=0)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    tag = models.ManyToManyField('Tag', related_name='POSTS', blank=True)
    draft = models.BooleanField(default=False)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.title}'

class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, blank=True, null=True)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, blank=True, null=True)
    text = models.TextField(max_length=300)
    date = models.DateTimeField(auto_now_add=True)
    comment_likes = models.IntegerField(default=0)
    comment_dislikes = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.author} - {self.post}'

class Tag(models.Model):
    text = models.CharField(max_length=64)

    def __str__(self):
        return self.text


class PostLike(models.Model):
    LIKE_OR_DISLAKE_CHOICES = (
        ("LIKE", "like"),
        ("DISLIKE", "dislike"),
        (None, "None")
    )

    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    for_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    like_or_dislike = models.CharField(max_length=7,
                                       choices=LIKE_OR_DISLAKE_CHOICES,
                                       default=None)

class CommentLike(models.Model):
    LIKE_OR_DISLAKE_CHOICES = (
        ("LIKE", "like"),
        ("DISLIKE", "dislike"),
        (None, "None")
    )

    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    for_com = models.ForeignKey(Comment, on_delete=models.CASCADE)
    like_or_dislike = models.CharField(max_length=7,
                                       choices=LIKE_OR_DISLAKE_CHOICES,
                                       default=None)


class Category(models.Model):
    name = models.CharField(max_length=48)

    def __str__(self):
        return f'{self.name}'


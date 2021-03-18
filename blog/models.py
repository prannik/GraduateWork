import os
from django.db import models
from django.urls import reverse
from django import forms

def get_upload_path(instance, filename):
    filename = instance.slug + '.' + filename.split('.')[1]
    return os.path.join('images/', filename)

class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=64, verbose_name='Заголовок')
    slug = models.SlugField(max_length=64, unique=True, db_index=True)
    text = models.TextField(verbose_name='Текст поста')
    date = models.DateTimeField(auto_now_add=True)
    post_likes = models.PositiveIntegerField(default=0)
    post_dislikes = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to=get_upload_path, blank=True, verbose_name='Картинка')
    tag = models.ManyToManyField('Tag', related_name='POSTS', blank=True)
    draft = models.BooleanField(default=False, verbose_name='Черновик')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, null=True, verbose_name='Категория')

    class Meta:
        ordering = ('title',)
        index_together = (('slug',),)
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.slug])


class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, blank=True, null=True)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, blank=True, null=True)
    text = models.TextField(max_length=300, verbose_name='Текст комментария')
    date = models.DateTimeField(auto_now_add=True)
    comment_likes = models.PositiveIntegerField(default=0)
    comment_dislikes = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ('post', 'author')
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'{self.author} - {self.post}'

class Tag(models.Model):
    text = models.CharField(max_length=64, verbose_name='Hashtag')

    def __str__(self):
        return f'{self.text}'


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
    name = models.CharField(max_length=150, db_index=True)
    slug = models.SlugField(max_length=150, unique=True, db_index=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('blog:cat_post_list', args=[self.slug])

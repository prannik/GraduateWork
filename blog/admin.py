from django.contrib import admin
from .models import Post, Comment, Category, Review


admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Review)

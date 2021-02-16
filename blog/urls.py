from django.urls import path
from .views import post_list, post_detail, post_new, post_edit, post_delete, post_like, post_dislike, post_comment, \
    comment_delete, comment_edit

urlpatterns = [
    path('', post_list, name='post_list'),
    path('list/', post_list, name='post_list'),
    path('new/', post_new, name='new'),
    path('detail/<int:post_pk>/', post_detail, name='post_detail'),
    path('edit/<int:post_pk>/', post_edit, name='post_edit'),
    path('delete/<int:post_pk>', post_delete, name='post_delete'),
    path('like/<int:post_pk>', post_like, name='post_like'),
    path('dislike/<int:post_pk>', post_dislike, name='post_dislike'),
    path('add_comment/<int:post_pk>', post_comment, name='post_comment'),
    path('comment_delete/<int:post_pk>/<int:comment_pk>', comment_delete, name='comment_delete'),
    path('comment_edit/<int:post_pk>/<int:comment_pk>', comment_edit, name='comment_edit'),
]

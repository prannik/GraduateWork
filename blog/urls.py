from django.urls import path
from .views import post_list, post_detail, post_new, post_edit, post_delete, post_comment, \
    comment_delete, comment_edit, tag_post, like_or_dislike, add_tag

urlpatterns = [
    path('', post_list, name='post_list'),
    path('list/', post_list, name='post_list'),
    path('new/', post_new, name='new'),
    path('detail/<int:post_pk>/', post_detail, name='post_detail'),
    path('edit/<int:post_pk>/', post_edit, name='post_edit'),
    path('delete/<int:post_pk>', post_delete, name='post_delete'),
    path('like_or_dislike/<int:post_pk>/<str:is_like>/', like_or_dislike, name='like_or_dislike'),

    path('add_comment/<int:post_pk>', post_comment, name='post_comment'),
    path('comment_delete/<int:post_pk>/<int:comment_pk>', comment_delete, name='comment_delete'),
    path('comment_edit/<int:post_pk>/<int:comment_pk>', comment_edit, name='comment_edit'),
    path('tag/<int:tag_pk>', tag_post, name='tag_post'),
    path('add_tag/<int:post_pk>', add_tag, name='add_tag')
]

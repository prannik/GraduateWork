from django.urls import path
from .views import post_list, post_detail, post_new, post_edit, post_delete, post_comment, \
    comment_delete, comment_edit, tag_post, post_like_or_dislike, tag_add, draft_list, \
    published_draft, tag_delete, cat_post_list, comment_like_or_dislike

urlpatterns = [
    path('', post_list, name='post_list'),

    path('list/', post_list, name='post_list'),
    path('cat_post_list/<int:cat_pk>', cat_post_list, name='cat_post_list'),
    path('draft_list/', draft_list, name='draft_list'),
    path('published_draft/<int:post_pk>', published_draft, name='published_draft'),

    path('new/', post_new, name='new'),
    path('detail/<int:post_pk>/', post_detail, name='post_detail'),
    path('edit/<int:post_pk>/', post_edit, name='post_edit'),
    path('delete/<int:post_pk>', post_delete, name='post_delete'),

    path('post_like_or_dislike/<int:post_pk>/<str:is_like>/<str:point>/',
         post_like_or_dislike, name='post_like_or_dislike'),

    path('comment_like_or_dislike/<int:post_pk>/<int:comment_pk>/<str:is_like>/',
         comment_like_or_dislike, name='comment_like_or_dislike'),

    path('add_comment/<int:post_pk>', post_comment, name='post_comment'),
    path('comment_delete/<int:post_pk>/<int:comment_pk>', comment_delete, name='comment_delete'),
    path('comment_edit/<int:post_pk>/<int:comment_pk>', comment_edit, name='comment_edit'),

    path('tag/<int:tag_pk>/', tag_post, name='tag_post'),
    path('tag_delete/<int:post_pk>/<int:tag_pk>/', tag_delete, name='tag_delete'),
    path('tag_add/<int:post_pk>/', tag_add, name='tag_add')
]

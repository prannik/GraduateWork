from django.urls import path
from .views import post_list, post_detail, post_new, post_edit, post_delete, post_comment, \
    comment_delete, comment_edit, tag_post, post_like_or_dislike, draft_list, \
    published_draft, tag_delete, cat_post_list, comment_like_or_dislike

urlpatterns = [

    path('list/', post_list, name='post_list'),
    path('cat_post_list/<str:slug>/', cat_post_list, name='cat_post_list'),
    path('draft_list/', draft_list, name='draft_list'),
    path('published_draft/<str:slug>/', published_draft, name='published_draft'),

    path('new/', post_new, name='new'),
    path('detail/<str:slug>/', post_detail, name='post_detail'),
    path('edit/<str:slug>/', post_edit, name='post_edit'),
    path('delete/<str:slug>/', post_delete, name='post_delete'),

    path('post_like_or_dislike/<str:slug>/<str:is_like>/<str:point>/',
         post_like_or_dislike, name='post_like_or_dislike'),

    path('comment_like_or_dislike/<str:slug>/<int:comment_pk>/<str:is_like>/',
         comment_like_or_dislike, name='comment_like_or_dislike'),

    path('add_comment/<str:slug>/', post_comment, name='post_comment'),
    path('comment_delete/<str:slug>/<int:comment_pk>', comment_delete, name='comment_delete'),
    path('comment_edit/<str:slug>/<int:comment_pk>', comment_edit, name='comment_edit'),

    path('tag/<int:tag_pk>/', tag_post, name='tag_post'),
    path('tag_delete/<str:slug>/<int:tag_pk>/', tag_delete, name='tag_delete'),

]

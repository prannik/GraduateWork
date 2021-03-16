from django.contrib import admin
from django.urls import path
from shop.views import product_list, product_detail, product_review, review_edit, review_delete, \
    review_like_or_dislike

app_name = 'shop'

urlpatterns = [
    path('', product_list, name='product_list'),
    path('<str:category_slug>/', product_list, name='product_list_by_category'),
    path('<int:id>/<str:slug>/', product_detail, name='product_detail'),

    path('review/<str:slug>/', product_review, name='product_review'),
    path('review_delete/<str:slug>/<int:review_pk>', review_delete, name='review_delete'),
    path('review_edit/<str:slug>/<int:review_pk>', review_edit, name='review_edit'),
    path('review_like_or_dislike/<str:slug>/<int:review_pk>/<str:is_like>/',
         review_like_or_dislike, name='review_like_or_dislike'),
]

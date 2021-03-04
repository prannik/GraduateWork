from django.urls import path
from .views import product_list, product_detail, product_review, review_edit, review_delete, review_like_or_dislike


urlpatterns = [
    path('product_list/', product_list, name='product_list'),
    path('product_detail/<int:product_pk>', product_detail, name='product_detail'),

    path('product_review/<int:product_pk>', product_review, name='product_review'),
    path('review_delete/<int:product_pk>/<int:review_pk>', review_delete, name='review_delete'),
    path('review_edit/<int:product_pk>/<int:review_pk>', review_edit, name='review_edit'),
    path('review_like_or_dislike/<int:product_pk>/<int:review_pk>/<str:is_like>/',
         review_like_or_dislike, name='review_like_or_dislike'),




]

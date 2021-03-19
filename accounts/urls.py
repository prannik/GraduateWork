from django.contrib.auth import views
from django.urls import path
from accounts.views import registration, user_login
from .decorators import check_recaptcha

urlpatterns = [
    path('login/', check_recaptcha(user_login), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('registration/', check_recaptcha(registration), name='registration')

]

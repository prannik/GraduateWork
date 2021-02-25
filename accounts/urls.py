from django.contrib.auth import views
from django.urls import path
from accounts.views import registration
from .decorators import check_recaptcha

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('registration/', check_recaptcha(registration), name='registration')

]

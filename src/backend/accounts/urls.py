from django.urls import path
from . import views

urlpatterns = [
    path('auth/register', views.UserRegister.as_view()),
    path('auth/reset-password-token/', views.UserResetPasswordToken.as_view()),
    path('auth/reset-password/', views.UserResetPassword.as_view()),
    path('auth/login/', views.UserLogin.as_view()),
    path('auth/logout/', views.UserLogout.as_view()),
    path('profile/', views.UserDetail.as_view()),
]
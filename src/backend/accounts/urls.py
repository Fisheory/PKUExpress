from django.urls import path, include
from . import views

urlpatterns = [
    # POST accounts/auth/* : 注册、获取验证码、重置密码、登录、登出
    path('auth/register', views.UserRegister.as_view()),
    path('auth/verification-code', views.VerificationCodeView.as_view()),
    path('auth/reset-password', views.UserResetPassword.as_view()),
    path('auth/login', views.UserLogin.as_view()),
    path('auth/logout', views.UserLogout.as_view()),
    
    # GET accounts/profile: 获取用户信息
    path('profile', views.UserDetail.as_view()),
    
    # GET accounts/profile/*-tasklist: 获取用户发布/接受/完成的任务列表
    path('profile/', include('tasks.urls')),
]
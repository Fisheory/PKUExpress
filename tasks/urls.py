from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_list),
    path('task-list/', views.task_list), # default st=0, en=10
    path('task-list/<int:st>/<int:en>/', views.task_list),
    path('<int:pk>/task-detail/', views.task_detail),
    path('task-create/', views.task_create),
    path('<int:pk>/task-accept/', views.task_accept),
    path('task-finish/', views.task_finish),
]
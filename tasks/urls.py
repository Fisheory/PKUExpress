from django.urls import path
from . import views

urlpatterns = [
    # GET tasks: 列出所有任务
    # POST tasks: 创建一个新任务
    path('', views.TaskList.as_view()), 

    # GET tasks/<int:pk>: 获取一个任务的详细信息
    # PUT tasks/<int:pk>: 更新一个任务
    path('<int:pk>', views.TaskDetail.as_view()),
]
from django.urls import path
from . import views

urlpatterns = [
    # GET tasks/tasklist: 列出所有任务
    #    参数: page = 页数
    #         size = 每页个数
    #         search = 搜索关键字 (可选)
    # POST tasks/tasklist: 创建一个新任务
    path("tasklist", views.TaskList.as_view()),
    # GET tasks/<int:pk>: 获取一个任务的详细信息
    # PATCH tasks/<int:pk>: 更新一个任务
    # DELETE tasks/<int:pk>: 删除一个任务
    path("tasklist/<int:pk>", views.TaskDetail.as_view()),
    # GET accounts/profile/*-tasklist: 获取用户发布/接受/完成的任务列表
    path("publish-tasklist", views.UserPublishedTaskList.as_view()),
    path("accept-tasklist", views.UserAcceptedTaskList.as_view()),
    path("finish-tasklist", views.UserFinishedTaskList.as_view()),
]

from django.urls import path
from . import views

urlpatterns = [
    # GET tasks: 列出所有任务
    #    参数: page = 页数
    #         size = 每页个数
    #         search = 搜索关键字 (可选)
    # POST tasks: 创建一个新任务
    path("tasklist", views.TaskList.as_view()),
    # GET tasks/<int:pk>: 获取一个任务的详细信息
    # PATCH tasks/<int:pk>: 更新一个任务
    # DELETE tasks/<int:pk>: 删除一个任务
    path("<int:pk>", views.TaskDetail.as_view()),
]

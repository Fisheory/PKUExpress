from django.urls import path
from . import views

urlpatterns = [
    path('task_list/<int:st>/<int:en>', views.task_list),
    path('<int:pk>/task_detail/', views.task_detail),
]
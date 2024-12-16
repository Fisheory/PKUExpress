from django.urls import path
from . import views

urlpatterns = [
    path("msglist", views.MessageList.as_view()),
]

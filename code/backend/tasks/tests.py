from django.test import TestCase

# 可能会用到
from accounts.models import CustomUser
from tasks.models import Task
from django.utils import timezone

import json

WORKER_MOST_ACCEPTED = 3

user1_data = {
    'username': 'user1',
    'password': 'abc87654321a',
    'email': 'example1@example.com',
    'phone': '1234567891',
}
user2_data = {
    'username': 'user2',
    'password': 'abc87654321b',
    'email': 'example2@example.com',
    'phone': '1234567892',
}
user3_data = {
    'username': 'user3',
    'password': 'abc87654321c',
    'email': 'example3@example.com',
    'phone': '1234567893',
}

register_url = '/accounts/register/'
login_url = '/accounts/login/'
task_create_url = '/tasks/task-create/'
task_detail_url = '/tasks/task-detail/'
task_list_url = '/tasks/task-list/'
task_accept_url = '/tasks/task-accept/'

# Create your tests here.

# Todo...
    
    

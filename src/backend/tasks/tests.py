from django.test import TestCase, Client

# 可能会用到
from accounts.models import CustomUser
from tasks.models import Task
from tasks.serializers import TaskSerializer
from django.utils import timezone
import time

import json

WORKER_MOST_ACCEPTED = 3

verification_code_url = "/accounts/auth/verification-code"
register_url = "/accounts/auth/register"
login_url = "/accounts/auth/login"
logout_url = "/accounts/auth/logout"
tasklist_url = "/tasks/tasklist"

user1 = {
    "username": "test1",
    "password": "passwordtest1",
    "email": "2200013000@pku.edu.cn",
    "phone": "12345678901",
}

user2 = {
    "username": "test2",
    "password": "passwordtest2",
    "email": "2200013100@stu.pku.edu.cn",
    "phone": "12345678902",
}

task1 = {
    "name": "task1",
    "description": "description1",
    "reward": 10,
    "end_location": "end_location1",
    "deadline": str(timezone.now() + timezone.timedelta(days=1)),
    "status": "to_be_accepted",
}

task2 = {
    "name": "task2",
    "description": "description2",
    "reward": 20,
    "end_location": "end_location2",
    "deadline": str(timezone.now() + timezone.timedelta(days=2)),
    "status": "to_be_accepted",
}

task3 = {
    "name": "task3",
    "description": "description3",
    "reward": 30,
    "end_location": "end_location3",
    "deadline": str(timezone.now() + timezone.timedelta(days=3)),
}

# Create your tests here.


class TaskTestCase(TestCase):
    def setUp(self):
        # 在每个测试函数执行之前执行
        # 创建用户
        self.user1 = CustomUser.objects.create_user(**user1)
        self.user2 = CustomUser.objects.create_user(**user2)
        # 创建任务
        self.task1 = Task.objects.create(publisher=self.user1, **task1)
        # 等待10ms
        time.sleep(0.01)
        self.task2 = Task.objects.create(publisher=self.user2, **task2)

    def test_list_tasks(self):
        """
        测试列出所有任务
        """
        client = Client()
        # 获取第一页任务
        get_params = {"page": 1, "size": 1}
        response = client.get(tasklist_url, data=get_params)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(len(response_data), 1)
        # print(response_data)
        self.assertEqual(response_data[0]["name"], task2["name"])

        # 获取第二页任务
        get_params = {"page": 2, "size": 1}
        response = client.get(tasklist_url, data=get_params)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(len(response_data), 1)
        # print(response_data)
        self.assertEqual(response_data[0]["name"], task1["name"])

    def test_create_task(self):
        """
        测试创建任务
        """
        client = Client()
        # 先登录
        response = client.post(login_url, data=user1)
        self.assertEqual(response.status_code, 200)
        token = response.json()["token"]
        # 创建任务
        response = client.post(
            tasklist_url,
            data=json.dumps(task3),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Token {token}",
        )
        self.assertEqual(response.status_code, 201)
        response_data = response.json()
        self.assertEqual(response_data["name"], task3["name"])
        self.assertEqual(response_data["publisher"], user1["username"])

    def test_get_task(self):
        """
        测试获取任务
        """
        client = Client()
        # 获取任务1
        response = client.get(f"{tasklist_url}/{self.task1.id}")
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data["name"], task1["name"])
        self.assertEqual(response_data["publisher"], user1["username"])

    def test_update_task(self):
        """
        测试更新任务
        """
        client = Client()
        # 先登录
        response = client.post(login_url, data=user2)
        self.assertEqual(response.status_code, 200)
        token = response.json()["token"]
        # 更新任务1
        response = client.patch(
            f"{tasklist_url}/{self.task1.id}",
            data=json.dumps({"status": "accepted"}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Token {token}",
        )
        self.assertEqual(response.status_code, 200)
        # 检查任务状态
        task = Task.objects.get(id=self.task1.id)
        self.assertEqual(task.status, "accepted")

    def test_delete_task(self):
        """
        测试用户本人删除任务
        """
        client = Client()
        # 先登录
        response = client.post(login_url, data=user1)
        self.assertEqual(response.status_code, 200)
        token = response.json()["token"]
        # 删除任务1
        response = client.delete(
            f"{tasklist_url}/{self.task1.id}",
            HTTP_AUTHORIZATION=f"Token {token}",
        )
        self.assertEqual(response.status_code, 200)
        # 检查任务是否被删除
        with self.assertRaises(Task.DoesNotExist):
            Task.objects.get(id=self.task1.id)

    def test_accept_task(self):
        """
        测试接受任务
        """
        client = Client()
        # 先登录
        response = client.post(login_url, data=user2)
        self.assertEqual(response.status_code, 200)
        token = response.json()["token"]
        # 接受任务1
        response = client.patch(
            f"{tasklist_url}/{self.task1.id}",
            data=json.dumps({"status": "accepted"}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Token {token}",
        )
        self.assertEqual(response.status_code, 200)
        # 检查任务状态
        task = Task.objects.get(id=self.task1.id)
        self.assertEqual(task.status, "accepted")
        self.assertEqual(task.worker, self.user2)

    def test_delete_other_user_task(self):
        """
        测试用户删除其他用户的任务
        """
        client = Client()
        # 先登录
        response = client.post(login_url, data=user2)
        self.assertEqual(response.status_code, 200)
        token = response.json()["token"]
        # 删除任务1
        response = client.delete(
            f"{tasklist_url}/{self.task1.id}",
            HTTP_AUTHORIZATION=f"Token {token}",
        )
        self.assertEqual(response.status_code, 403)
        # 检查任务是否被删除
        task = Task.objects.get(id=self.task1.id)
        self.assertEqual(task.status, "to_be_accepted")

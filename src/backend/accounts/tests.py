from django.test import TestCase, Client
from django.core import mail
from django.conf import settings
import json
import re
from .models import CustomUser

# Create your tests here.

"""
测试了用户注册, 登录, 获取用户信息, 登出四个接口.

测试: python manage.py test accounts
"""

DEFALUT_GOLD = 1000
user_data = {
    "username": "test_user",
    "password": "abc87654321",
    "email": "example@stu.pku.edu.cn",
    "phone": "13640486555",
}
user_login_data = {
    "email": "example@stu.pku.edu.cn",
    "password": "abc87654321",
}
verification_code_url = "/accounts/auth/verification-code"
regiter_url = "/accounts/auth/register"
login_url = "/accounts/auth/login"
detail_url = "/accounts/profile"
logout_url = "/accounts/auth/logout"


class UserRegisterTestCase(TestCase):
    """
    测试用户注册功能
    """

    def setUp(self):
        # 每个测试用例执行前都会执行setUp方法
        self.client = Client()

    # def tearDown(self):
    # 每个测试用例执行后都会执行tearDown方法

    def test_register_valid(self):
        """
        测试注册成功的情况
        """
        # 首先获取验证码
        response = self.client.post(
            verification_code_url,
            data=json.dumps({"email": user_data["email"], "usage": "register"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        # 从邮箱中找到验证码
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        self.assertEqual(email.to[0], user_data["email"])
        match = re.findall(r"\d{6}", email.body)
        self.assertEqual(len(match), 1)
        verification_code = match[0]
        # print("verification code = {code}".format(code=verification_code))
        # 注册
        response = self.client.post(
            regiter_url,
            data=json.dumps({**user_data, "verification_code": verification_code}),
            content_type="application/json",
        )
        # print(response.json())
        self.assertEqual(response.status_code, 201)

    def test_register_invalid_email(self):
        """
        测试邮箱格式不正确的情况
        """
        response = self.client.post(
            verification_code_url,
            data=json.dumps({"email": "invalid_email", "usage": "register"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

    def test_register_invalid_verification_code(self):
        """
        测试验证码不正确的情况
        """
        response = self.client.post(
            verification_code_url,
            data=json.dumps({"email": user_data["email"], "usage": "register"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        response = self.client.post(
            regiter_url,
            data=json.dumps({**user_data, "verification_code": "invalid_code"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

    def test_register_empty_username(self):
        """
        测试用户名为空的情况
        """
        # 先获取验证码
        response = self.client.post(
            verification_code_url,
            data=json.dumps({"email": user_data["email"], "usage": "register"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        # 注册
        temp_user_data = user_data.copy()
        temp_user_data["username"] = ""
        response = self.client.post(
            regiter_url,
            data=json.dumps(temp_user_data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

    def test_register_empty_password(self):
        """
        测试密码为空的情况
        """
        # 先获取验证码
        response = self.client.post(
            verification_code_url,
            data=json.dumps({"email": user_data["email"], "usage": "register"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        # 注册
        temp_user_data = user_data.copy()
        temp_user_data["password"] = ""
        response = self.client.post(
            regiter_url,
            data=json.dumps(temp_user_data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

    def test_register_username_exists(self):
        """
        测试用户名已存在的情况
        """
        # 先在模型中添加一个用户
        CustomUser.objects.create_user(**user_data)
        # 获取验证码
        response = self.client.post(
            verification_code_url,
            data=json.dumps({"email": user_data["email"], "usage": "register"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)


class UserLoginTestCase(TestCase):
    """
    测试用户登录功能
    """

    def setUp(self):
        self.client = Client()
        # 先添加一个用户
        CustomUser.objects.create_user(**user_data)

    def test_login_valid(self):
        """
        测试登录成功的情况
        """
        # 登录
        response = self.client.post(
            login_url,
            data=json.dumps(user_login_data),
            content_type="application/json",
        )
        # print(response.json())
        self.assertEqual(response.status_code, 200)
        self.assertTrue("token" in response.json())
        # print(response.json()["token"])

    def test_login_empty_email(self):
        """
        测试登录时邮箱为空的情况
        """
        response = self.client.post(
            login_url,
            data=json.dumps({"email": "", "password": "password"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["msg"], "empty email or password")

    def test_login_empty_password(self):
        """
        测试登录时密码为空的情况
        """
        response = self.client.post(
            login_url,
            data=json.dumps({"email": "email", "password": ""}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["msg"], "empty email or password")

    def test_login_wrong_password(self):
        """
        测试登录时密码错误的情况
        """
        # 登录
        response = self.client.post(
            login_url,
            data=json.dumps(
                {"email": user_data["email"], "password": "wrong_password"}
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["msg"], "invalid password")


class UserResetPasswordTestCase(TestCase):
    """
    测试用户重置密码功能
    """

    def setUp(self):
        self.client = Client()
        # 先添加一个用户
        CustomUser.objects.create_user(**user_data)

    def test_reset_password_valid(self):
        """
        测试重置密码成功的情况
        """
        # 先获取验证码
        response = self.client.post(
            verification_code_url,
            data=json.dumps({"email": user_data["email"], "usage": "reset"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        # 从邮箱中找到验证码
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        self.assertEqual(email.to[0], user_data["email"])
        match = re.findall(r"\d{6}", email.body)
        self.assertEqual(len(match), 1)
        verification_code = match[0]
        # 重置密码
        response = self.client.post(
            "/accounts/auth/reset-password",
            data=json.dumps(
                {
                    "email": user_data["email"],
                    "verification_code": verification_code,
                    "password": "new_password",
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        # 重置密码后登录
        response = self.client.post(
            login_url,
            data=json.dumps({"email": user_data["email"], "password": "new_password"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

    def test_reset_password_invalid_email(self):
        """
        测试邮箱格式不正确的情况
        """
        response = self.client.post(
            verification_code_url,
            data=json.dumps({"email": "invalid_email", "usage": "reset"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

    def test_reset_password_invalid_verification_code(self):
        """
        测试验证码不正确的情况
        """
        response = self.client.post(
            verification_code_url,
            data=json.dumps({"email": user_data["email"], "usage": "reset"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        response = self.client.post(
            "/accounts/auth/reset-password",
            data=json.dumps(
                {
                    "email": user_data["email"],
                    "verification_code": "invalid_code",
                    "password": "new_password",
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)


class UserDetailTestCase(TestCase):
    """
    测试获取用户信息功能
    """

    def setUp(self):
        self.client = Client()
        # 先添加一个用户
        CustomUser.objects.create_user(**user_data)

    def test_get_user_detail(self):
        """
        测试成功获取用户信息
        """
        # 先登录
        response = self.client.post(
            login_url,
            data=json.dumps(user_login_data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        token = response.json()["token"]
        # 获取用户信息
        response = self.client.get(
            detail_url,
            HTTP_AUTHORIZATION="Token {token}".format(token=token),
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["username"], user_data["username"])
        self.assertEqual(response.json()["email"], user_data["email"])
        self.assertEqual(response.json()["phone"], user_data["phone"])
        self.assertEqual(response.json()["gold"], DEFALUT_GOLD)

    def test_get_user_detail_without_token(self):
        """
        测试未登录时获取用户信息
        """
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, 401)

    def test_get_user_detail_invalid_token(self):
        """
        测试无效token时获取用户信息
        """
        response = self.client.get(
            detail_url,
            HTTP_AUTHORIZATION="Token invalid_token",
        )
        self.assertEqual(response.status_code, 401)

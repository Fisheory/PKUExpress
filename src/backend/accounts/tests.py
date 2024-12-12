from django.test import TestCase

import json

# Create your tests here.

"""
测试了用户注册, 登录, 获取用户信息, 登出四个接口.

测试: python manage.py test accounts
"""

DEFALUT_GOLD = 1000
user_data = {
    "username": "test",
    "password": "abc87654321",
    "email": "example@example.com",
    "phone": "1234567890",
}
user_login_data = {
    "username": "test",
    "password": "abc87654321",
}
regiter_url = "/accounts/auth/register/"
login_url = "/accounts/auth/login/"
detail_url = "/accounts/profile/"
logout_url = "/accounts/auth/logout/"


class UserRegisterTestCase(TestCase):

    def test_register_valid(self):

        response = self.client.post(
            regiter_url, data=json.dumps(user_data), content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)

    def test_register_empty_username(self):

        temp_user_data = user_data.copy()
        temp_user_data["username"] = ""
        response = self.client.post(
            regiter_url,
            data=json.dumps(temp_user_data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

    def test_register_empty_password(self):

        temp_user_data = user_data.copy()
        temp_user_data["password"] = ""
        response = self.client.post(
            regiter_url,
            data=json.dumps(temp_user_data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

    def test_register_username_exists(self):

        self.client.post(
            regiter_url, data=json.dumps(user_data), content_type="application/json"
        )
        response = self.client.post(
            regiter_url, data=json.dumps(user_data), content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)

    def test_register_method_not_allowed(self):

        response = self.client.get(regiter_url)
        self.assertEqual(response.status_code, 405)


class UserLoginTestCase(TestCase):

    def setUp(self):

        self.token = ""

    def test_login_valid(self):

        # 由于每个单元测试都是独立的, 所以要先注册. 后面同理
        self.client.post(
            regiter_url, data=json.dumps(user_data), content_type="application/json"
        )
        response = self.client.post(
            "/accounts/login/",
            data=json.dumps(user_login_data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.token = response.json()["token"]
        self.assertTrue(self.token)

    def test_login_empty_username(self):

        self.client.post(
            regiter_url, data=json.dumps(user_data), content_type="application/json"
        )
        temp_user_login_data = user_login_data.copy()
        temp_user_login_data["username"] = ""
        response = self.client.post(
            login_url,
            data=json.dumps(temp_user_login_data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

    def test_login_empty_password(self):

        self.client.post(
            regiter_url, data=json.dumps(user_data), content_type="application/json"
        )
        temp_user_login_data = user_login_data.copy()
        temp_user_login_data["password"] = ""
        response = self.client.post(
            login_url,
            data=json.dumps(temp_user_login_data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

    def test_login_username_not_exists(self):

        self.client.post(
            regiter_url, data=json.dumps(user_data), content_type="application/json"
        )
        temp_user_login_data = user_login_data.copy()
        temp_user_login_data["username"] = "notexists"
        response = self.client.post(
            login_url,
            data=json.dumps(temp_user_login_data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

    def test_login_password_invalid(self):

        self.client.post(
            regiter_url, data=json.dumps(user_data), content_type="application/json"
        )
        temp_user_login_data = user_login_data.copy()
        temp_user_login_data["password"] = "invalid"
        response = self.client.post(
            login_url,
            data=json.dumps(temp_user_login_data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

    def test_login_method_not_allowed(self):

        response = self.client.get(login_url)
        self.assertEqual(response.status_code, 405)


class UserDetailTestCase(TestCase):

    def setUp(self):

        self.token = ""

    def test_detail_valid(self):

        self.client.post(
            regiter_url, data=json.dumps(user_data), content_type="application/json"
        )
        response = self.client.post(
            login_url, data=json.dumps(user_login_data), content_type="application/json"
        )
        self.token = response.json()["token"]
        self.assertTrue(self.token)

        response = self.client.get(detail_url, HTTP_AUTHORIZATION="Token " + self.token)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["username"], user_data["username"])
        self.assertEqual(response.json()["email"], user_data["email"])
        self.assertEqual(response.json()["phone"], user_data["phone"])
        self.assertEqual(response.json()["gold"], DEFALUT_GOLD)

    def test_detail_unauthorized(self):

        self.client.post(
            regiter_url, data=json.dumps(user_data), content_type="application/json"
        )
        response = self.client.post(
            login_url, data=json.dumps(user_login_data), content_type="application/json"
        )
        self.token = response.json()["token"]
        self.assertTrue(self.token)

        response = self.client.post(detail_url, HTTP_AUTHORIZATION="Token " + "invalid")
        self.assertEqual(response.status_code, 401)

    def test_detail_method_not_allowed(self):

        self.client.post(
            regiter_url, data=json.dumps(user_data), content_type="application/json"
        )
        response = self.client.post(
            login_url, data=json.dumps(user_login_data), content_type="application/json"
        )
        self.token = response.json()["token"]
        self.assertTrue(self.token)

        response = self.client.post(
            detail_url, HTTP_AUTHORIZATION="Token " + self.token
        )
        self.assertEqual(response.status_code, 405)


class UserLogoutTestCase(TestCase):

    def setUp(self):

        self.token = ""

    def test_logout_valid(self):

        self.client.post(
            regiter_url, data=json.dumps(user_data), content_type="application/json"
        )
        response = self.client.post(
            login_url, data=json.dumps(user_login_data), content_type="application/json"
        )
        self.token = response.json()["token"]
        self.assertTrue(self.token)

        response = self.client.post(
            logout_url, HTTP_AUTHORIZATION="Token " + self.token
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.get(logout_url, HTTP_AUTHORIZATION="Token " + self.token)
        self.assertEqual(response.status_code, 401)

    def test_logout_unauthorized(self):

        self.client.post(
            regiter_url, data=json.dumps(user_data), content_type="application/json"
        )
        response = self.client.post(
            login_url, data=json.dumps(user_login_data), content_type="application/json"
        )
        self.token = response.json()["token"]
        self.assertTrue(self.token)

        response = self.client.post(logout_url, HTTP_AUTHORIZATION="Token " + "invalid")
        self.assertEqual(response.status_code, 401)

    def test_logout_method_not_allowed(self):

        self.client.post(
            regiter_url, data=json.dumps(user_data), content_type="application/json"
        )
        response = self.client.post(
            login_url, data=json.dumps(user_login_data), content_type="application/json"
        )
        self.token = response.json()["token"]
        self.assertTrue(self.token)

        response = self.client.get(logout_url, HTTP_AUTHORIZATION="Token " + self.token)
        self.assertEqual(response.status_code, 405)

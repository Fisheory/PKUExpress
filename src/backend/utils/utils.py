from django.core.mail import send_mail
from django.contrib.auth.backends import BaseBackend

from rest_framework.views import exception_handler

from accounts.models import CustomUser


class EmailBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = CustomUser.objects.get(email=email)
            if user.check_password(password):
                return user
        except CustomUser.DoesNotExist:
            return None
        return None


def msg_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        response.data = {"msg": str(exc)}
    return response


def send_email(email, token):
    try:
        send_mail(
            subject="PKUExpress 验证码",
            message=f"您的验证码为{token}, 有效时间为5分钟",
            from_email="pkuexpress@qq.com",
            recipient_list=[email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print("send email error: ", e)
        return False
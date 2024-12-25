from django.core.mail import send_mail


def send_email(email, token):
    try:
        send_mail(
            subject="PKUExpress 验证码",
            message=f"您的验证码为{token}, 有效时间为5分钟",
            from_email="2102008267@qq.com",
            recipient_list=[email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print("send email error: ", e)
        return False

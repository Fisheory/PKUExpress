import random
import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate

from rest_framework import status as http_status
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes

from .serializers import CustomUserSerializer, VerificationCodeSerializer
from .models import CustomUser, VerificationCode


class UserRegister(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context


class UserLogin(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return JsonResponse(
                {"msg": "empty email or password"},
                status=http_status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(email=email, password=password)
        if user is None:
            return JsonResponse(
                {"msg": "invalid password"},
                status=http_status.HTTP_400_BAD_REQUEST,
            )
        else:
            token, _ = Token.objects.get_or_create(user=user)
            return JsonResponse(
                {
                    "msg": "login success",
                    "token": token.key,
                    "username": user.username,
                },
                status=http_status.HTTP_200_OK,
            )


class UserLogout(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        Token.objects.filter(user=request.user).delete()
        return JsonResponse(
            {"msg": "logout success"},
            status=http_status.HTTP_200_OK,
        )


class UserDetail(RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class VerificationCodeView(CreateAPIView):
    queryset = VerificationCode.objects.all()
    serializer_class = VerificationCodeSerializer
    permission_classes = [AllowAny]


class UserResetPassword(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        email = data.get("email")
        token = data.get("verification_code")
        password = data.get("password")

        if not CustomUser.objects.filter(email=email).exists():
            return JsonResponse(
                {"msg": "email does not exist"},
                status=http_status.HTTP_400_BAD_REQUEST,
            )

        verification_code = (
            VerificationCode.objects.filter(email=email, token=token, usage="reset")
            .order_by("-create_time")
            .first()
        )

        if verification_code is not None and verification_code.is_valid():
            user = CustomUser.objects.get(email=email)
            user.set_password(password)
            user.save()

            # 更改密码后删除之前的登录凭据token, 相当于登出
            Token.objects.filter(user=user).delete()

            # 验证码token也删除
            verification_code.delete()

            return JsonResponse(
                {"msg": "password reset"},
                status=http_status.HTTP_200_OK,
            )
        else:
            return JsonResponse(
                {"msg": "invalid token"},
                status=http_status.HTTP_400_BAD_REQUEST,
            )

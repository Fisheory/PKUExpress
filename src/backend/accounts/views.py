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

<<<<<<< HEAD
from .serializers import CustomUserSerializer, PasswordTokenSerializer
from .models import CustomUser, PasswordToken
=======
from .serializers import CustomUserSerializer, VerificationCodeSerializer
from .models import CustomUser, VerificationCode

>>>>>>> ac4d57e3eaba250c9fdd3cb468a030d322ac2ae9

class UserRegister(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]
<<<<<<< HEAD
    
class UserLogin(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        data = request.data
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return JsonResponse({'status': 'error', 'msg': 'empty email or password'},
                                status=http_status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(email=email, password=password)
        if user is None:
            return JsonResponse({'status': 'error', 'msg': 'invalid password'}, 
                                status=http_status.HTTP_400_BAD_REQUEST)
        else:
            token, _ = Token.objects.get_or_create(user=user) 
            return JsonResponse({'status': 'success', 'msg': 'login success',
                                 'token': token.key, 'username': user.username},
                                status=http_status.HTTP_200_OK)
            
class UserLogout(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        Token.objects.filter(user=request.user).delete()
        return JsonResponse({'status': 'success', 'msg': 'logout success'},
                            status=http_status.HTTP_200_OK)
=======

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

>>>>>>> ac4d57e3eaba250c9fdd3cb468a030d322ac2ae9

class UserDetail(RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]
<<<<<<< HEAD
    
    def get_object(self):
        return self.request.user

class UserResetPasswordToken(CreateAPIView):
    queryset = PasswordToken.objects.all()
    serializer_class = PasswordTokenSerializer
    permission_classes = [AllowAny]

class UserResetPassword(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        data = request.data
        email = data.get('email')
        token = data.get('token')
        password = data.get('password')
        
        if not CustomUser.objects.filter(email=email).exists():
            return JsonResponse({'status': 'error', 'msg': 'email does not exist'},
                                status=http_status.HTTP_400_BAD_REQUEST)
            
        token_obj = PasswordToken.objects.filter(
            email=email, 
            token=token, 
            usage='reset'
        ).order_by('-create_time').first()
        
        if token_obj is not None and token_obj.is_valid():
            user = CustomUser.objects.get(email=email)
            user.set_password(password)
            user.save()
            
            # 更改密码后删除之前的登录凭据token, 相当于登出
            Token.objects.filter(user=user).delete()
            
            # 验证码token也删除
            PasswordToken.objects.filter(email=email).delete()
            
            return JsonResponse({'status': 'success', 'msg': 'password reset'},
                                status=http_status.HTTP_200_OK)
        else:
            return JsonResponse({'status': 'error', 'msg': 'invalid token'},
                                status=http_status.HTTP_400_BAD_REQUEST)
=======

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
>>>>>>> ac4d57e3eaba250c9fdd3cb468a030d322ac2ae9


# Create your views here.
@csrf_exempt
<<<<<<< HEAD
@api_view(['POST'])
def register_view(request):
    '''
    Todo: 验证方式? (优先级不高)
          密码的传输?
    
=======
@api_view(["POST"])
def register_view(request):
    """
    Todo: 验证方式? (优先级不高)
          密码的传输?

>>>>>>> ac4d57e3eaba250c9fdd3cb468a030d322ac2ae9
    用户状态：未登录
    简介: 注册视图, 接受信息并注册新用户
    注意: 不带Authorization的Header, 否则可能会因为token验证失败而返回401
          以email作为唯一标识, 不允许重复注册
<<<<<<< HEAD
    
=======

>>>>>>> ac4d57e3eaba250c9fdd3cb468a030d322ac2ae9
    URL: /accounts/register/
    Method: POST
    Header: Content-Type: application/json
    Body: JSON {
        "email": "email",
        "username": "username",
        "password": "password",
        "phone": "phone" (optional)
    }
<<<<<<< HEAD
    Response: 
        Success: Code 200 JSON {'status': 'success', 'msg': 'register success'}
        Error: Code 400 JSON {'status': 'error', 'msg': 'error message'}
               Code 405: Method Not Allowed
    '''
=======
    Response:
        Success: Code 200 JSON {'status': 'success', 'msg': 'register success'}
        Error: Code 400 JSON {'status': 'error', 'msg': 'error message'}
               Code 405: Method Not Allowed
    """
>>>>>>> ac4d57e3eaba250c9fdd3cb468a030d322ac2ae9
    data = json.loads(request.body)

    serializer = CustomUserSerializer(data=data)
    # 判断是否合法放在serializer中进行
    try:
        if serializer.is_valid(raise_exception=True):
            serializer.save()
<<<<<<< HEAD
            return JsonResponse({'status': 'success', 'msg': 'register success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'msg': str(e)}, status=400)

    
@csrf_exempt
@api_view(['POST'])
def login_view(request):
    '''
=======
            return JsonResponse({"msg": "register success"})
    except Exception as e:
        return JsonResponse({"msg": str(e)}, status=400)


@csrf_exempt
@api_view(["POST"])
def login_view(request):
    """
>>>>>>> ac4d57e3eaba250c9fdd3cb468a030d322ac2ae9
    用户状态：未登录
    简介: 登录视图, 接受信息并登录用户, 返回token
    注意: 登录时不带Authorization的Header, 否则可能会因为token验证失败而返回401
          保存返回的token, 用于后续验证用户身份
<<<<<<< HEAD
    
=======

>>>>>>> ac4d57e3eaba250c9fdd3cb468a030d322ac2ae9
    URL: /accounts/login/
    Method: POST
    Header: Content-Type: application/json
    Body: JSON {
        "email": "email",
        "password": "password"
    }
    Response:
        Success: Code 200 JSON {'status': 'success', 'msg': 'login success', 'token': 'token'}
        Error: Code 400 JSON {'status': 'error', 'msg': 'error message'}
               Code 405: Method Not Allowed
<<<<<<< HEAD
    '''
    data = json.loads(request.body)
    email = data.get('email')
    password = data.get('password')
        
    if not email or not password:
        return JsonResponse({'status': 'error', 'msg': 'empty email or password'}, status=400)
    if not CustomUser.objects.filter(email=email).exists():
        return JsonResponse({'status': 'error', 'msg': 'email does not exist'}, status=400)
        
    user = authenticate(email=email, password=password)
    if user is None:
        return JsonResponse({'status': 'error', 'msg': 'invalid password'}, status=400)
    else:
        token, _ = Token.objects.get_or_create(user=user) 
        # print(token.key)
        return JsonResponse({'status': 'success', 'msg': 'login success',
                             'token': token.key, 'username': user.username})
    
@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    '''
=======
    """
    data = json.loads(request.body)
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return JsonResponse(
            {"status": "error", "msg": "empty email or password"}, status=400
        )
    if not CustomUser.objects.filter(email=email).exists():
        return JsonResponse(
            {"status": "error", "msg": "email does not exist"}, status=400
        )

    user = authenticate(email=email, password=password)
    if user is None:
        return JsonResponse({"status": "error", "msg": "invalid password"}, status=400)
    else:
        token, _ = Token.objects.get_or_create(user=user)
        # print(token.key)
        return JsonResponse(
            {
                "status": "success",
                "msg": "login success",
                "token": token.key,
                "username": user.username,
            }
        )


@csrf_exempt
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """
>>>>>>> ac4d57e3eaba250c9fdd3cb468a030d322ac2ae9
    用户状态：已登录
    简介: 登出视图, 接受信息并登出用户, 删除token
    注意: 需要在Header中加入 key=Authorization, value=Token token, 其中token为登录时返回的token, 空格分隔
          例如："Authorization": "Token b911f5e08e7c52826ebecee5ff63bf1895922f4c"
<<<<<<< HEAD
          
=======

>>>>>>> ac4d57e3eaba250c9fdd3cb468a030d322ac2ae9
    URL: /accounts/logout/
    Method: POST
    Header: Content-Type: application/json, Authorization: Token token
    Body: JSON {}
    Response:
        Success: Code 200 JSON {'status': 'success', 'msg': 'logout success'}
        Error: Code 400 JSON {'status': 'error', 'msg': 'error message'}
               Code 401: Unauthorized
               Code 405: Method Not Allowed
<<<<<<< HEAD
    '''
    Token.objects.filter(user=request.user).delete()
    return JsonResponse({'status': 'success', 'msg': 'logout success'})

    
@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def CustomUserDetail(request):
    '''
    用户状态：已登录
    简介: 获取当前登录用户信息
    
=======
    """
    Token.objects.filter(user=request.user).delete()
    return JsonResponse({"msg": "logout success"})


@csrf_exempt
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def CustomUserDetail(request):
    """
    用户状态：已登录
    简介: 获取当前登录用户信息

>>>>>>> ac4d57e3eaba250c9fdd3cb468a030d322ac2ae9
    URL: /accounts/user/
    Method: GET
    Header: Content-Type: application/json, Authorization: Token token
    Body: JSON {}
    Response:
        Success: Code 200 JSON {
            "username": "username",
            "email": "email",
            "phone": "phone",
            "gold": "gold",
            "published_tasks": [(task1), (task2), ...],
            "accepted_tasks": [(task1), (task2), ...],
            ...
        }
        Error: Code 400 JSON {'status': 'error', 'msg': 'error message'}
               Code 401: Unauthorized
               Code 405: Method Not Allowed
<<<<<<< HEAD
    '''
=======
    """
>>>>>>> ac4d57e3eaba250c9fdd3cb468a030d322ac2ae9
    email = request.user.email
    user = CustomUser.objects.get(email=email)
    serializer = CustomUserSerializer(user)
    return JsonResponse(serializer.data)

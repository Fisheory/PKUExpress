from django.http import JsonResponse
from .models import CustomUser
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout

from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view

from .serializers import CustomUserSerializer

import json

# Create your views here.
@csrf_exempt
@api_view(['POST'])
def register_view(request):
    '''
    注册视图, 接受信息并注册新用户
    
    URL: /accounts/register/
    Method: POST
    Header: Content-Type: application/json
    Body: JSON {
        "username": "username",
        "password": "password",
        "email": "email", (optional)
        "phone": "phone" (optional)
    }
    Response: 
        Success: Code 200 JSON {'status': 'success', 'msg': 'register success'}
        Error: Code 400 JSON {'status': 'error', 'msg': 'error message'}
               Code 405 JSON {'status': 'error', 'msg': 'invalid request method'}
    '''
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data['username']
        password = data['password'] #
        
        if not username or not password:
            return JsonResponse({'status': 'error', 'msg': 'empty username or password'}, status=400)
        if CustomUser.objects.filter(username=username).exists():
            return JsonResponse({'status': 'error', 'msg': 'username already exists'}, status=400)
        
        serializer = CustomUserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'status': 'success', 'msg': 'register success'})

    
@csrf_exempt
@api_view(['POST'])
def login_view(request):
    '''
    登录视图, 接受信息并登录用户, 返回token
    注意: 保存返回的token, 用于后续验证用户身份
    
    URL: /accounts/login/
    Method: POST
    Header: Content-Type: application/json
    Body: JSON {
        "username": "username",
        "password": "password"
    }
    Response:
        Success: Code 200 JSON {'status': 'success', 'msg': 'login success', 'token': 'token'}
        Error: Code 400 JSON {'status': 'error', 'msg': 'error message'}
               Code 405 JSON {'status': 'error', 'msg': 'invalid request method'}
    '''
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data['username']
        password = data['password']
        
        if not username or not password:
            return JsonResponse({'status': 'error', 'msg': 'empty username or password'}, status=400)
        if not CustomUser.objects.filter(username=username).exists():
            return JsonResponse({'status': 'error', 'msg': 'username does not exist'}, status=400)
        
        user = authenticate(username=username, password=password)
        if user is None:
            return JsonResponse({'status': 'error', 'msg': 'invalid password'}, status=400)
        else:
            token, _ = Token.objects.get_or_create(user=user) 
            # print(token.key)
            return JsonResponse({'status': 'success', 'msg': 'login success', 'token': token.key})
    
@csrf_exempt
@api_view(['POST'])
def logout_view(request):
    '''
    用户状态：已登录
    登出视图, 接受信息并登出用户, 删除token
    注意: 需要在Header中加入 key=Authorization, value=Token token, 其中token为登录时返回的token, 空格分隔
          例如："Authorization": "Token b911f5e08e7c52826ebecee5ff63bf1895922f4c"
          
    URL: /accounts/logout/
    Method: POST
    Header: Content-Type: application/json, Authorization: Token token
    Body: JSON {}
    Response:
        Success: Code 200 JSON {'status': 'success', 'msg': 'logout success'}
        Error: Code 400 JSON {'status': 'error', 'msg': 'error message'}
               Code 405 JSON {'status': 'error', 'msg': 'invalid request method'}
    '''
    if request.method == 'POST':
        if request.user.is_authenticated:
            Token.objects.filter(user=request.user).delete()
            return JsonResponse({'status': 'success', 'msg': 'logout success'})
        else:
            return JsonResponse({'status': 'error', 'msg': 'user not logged in'}, status=400)
    
@csrf_exempt
@api_view(['GET'])
def CustomUserDetail(request):
    '''
    用户状态：已登录
    获取当前登录用户信息
    
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
            "accepted_tasks": [(task)]
        }
        Error: Code 400 JSON {'status': 'error', 'msg': 'error message'}
               Code 405 JSON {'status': 'error', 'msg': 'invalid request method'}
    '''
    if request.user.is_authenticated:
        username = request.user.username
        user = CustomUser.objects.get(username=username)
        serializer = CustomUserSerializer(user)
        return JsonResponse(serializer.data)
    else:
        return JsonResponse({'status': 'error', 'msg': 'user not logged in'}, status=400)
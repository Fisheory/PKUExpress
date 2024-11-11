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
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data['username']
        password = data['password'] #
        
        if not username or not password:
            return JsonResponse({'status': 'error', 'msg': 'empty username or password'}, status=400)
        if CustomUser.objects.filter(username=username).exists():
            return JsonResponse({'status': 'error', 'msg': 'username already exists'}, status=400)
        
        user = CustomUser.objects.create_user(
            username=username, password=password)
        user.save()
        token = Token.objects.create(user=user)
        # print(token.key)
        return JsonResponse({'status': 'success', 'msg': 'register success'})
    else:
        return JsonResponse({'status': 'error', 'msg': 'invalid request method'}, status=400)
    
@csrf_exempt
@api_view(['POST'])
def login_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data['username']
        password = data['password']
        
        if not username or not password:
            return JsonResponse({'status': 'error', 'msg': 'empty username or password'})
        if not CustomUser.objects.filter(username=username).exists():
            return JsonResponse({'status': 'error', 'msg': 'username does not exist'})
        
        user = authenticate(username=username, password=password)
        if user is None:
            return JsonResponse({'status': 'error', 'msg': 'invalid password'})
        else:
            login(request, user)  
            token = Token.objects.get(user=user) 
            # print(token.key)
            return JsonResponse({'status': 'success', 'msg': 'login success', 'token': token.key})
    else:
        return JsonResponse({'status': 'error', 'msg': 'invalid request method'})
    
@csrf_exempt
@api_view(['POST'])
def logout_view(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            logout(request)
            return JsonResponse({'status': 'success', 'msg': 'logout success'})
        else:
            return JsonResponse({'status': 'error', 'msg': 'user not logged in'})
    else:
        return JsonResponse({'status': 'error', 'msg': 'invalid request method'})
    
@csrf_exempt
@api_view(['GET'])
def CustomUserDetail(request):
    if request.user.is_authenticated:
        username = request.user.username
        user = CustomUser.objects.get(username=username)
        serializer = CustomUserSerializer(user)
        return JsonResponse(serializer.data)
    else:
        return JsonResponse({'status': 'error', 'msg': 'user not logged in'})
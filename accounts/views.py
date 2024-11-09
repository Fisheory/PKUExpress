from django.shortcuts import render
from django.http import JsonResponse
from .models import CustomUser
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
import json

# Create your views here.
@csrf_exempt
def register_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data['username']
        password = data['password'] #
        
        if not username or not password:
            return JsonResponse({'status': 'error', 'msg': 'empty username or password'})
        if CustomUser.objects.filter(username=username).exists():
            return JsonResponse({'status': 'error', 'msg': 'username already exists'})
        
        user = CustomUser.objects.create_user(
            username=username, password=password)
        user.save()
        return JsonResponse({'status': 'success', 'msg': 'register success'})
    else:
        return JsonResponse({'status': 'error', 'msg': 'invalid request method'})
    
@csrf_exempt
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
        elif user.is_authenticated:
            return JsonResponse({'status': 'error', 'msg': 'user already logged in'})
        else:
            login(request, user)  
            return JsonResponse({'status': 'success', 'msg': 'login success'})
    else:
        return JsonResponse({'status': 'error', 'msg': 'invalid request method'})
    
@csrf_exempt
def logout_view(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            logout(request)
            return JsonResponse({'status': 'success', 'msg': 'logout success'})
        else:
            return JsonResponse({'status': 'error', 'msg': 'user not logged in'})
    else:
        return JsonResponse({'status': 'error', 'msg': 'invalid request method'})
    

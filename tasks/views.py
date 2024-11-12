from .models import Task
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from .serializers import TaskSerializer

import json

# Create your views here.
@csrf_exempt
@api_view(['GET'])
def task_list(request,st,en):
    if request.method == 'GET':
        tasks = Task.objects.all()[st:en]
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)
    else:
        return Response(status=405)
    
@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def task_detail(request, pk):
    try:
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        return Response(status=404)
    
    if request.method == 'GET':
        serializer = TaskSerializer(task)
        return Response(serializer.data)
    else:
        return Response(status=405)

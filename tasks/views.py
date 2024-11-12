from .models import Task
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import TaskSerializer

import json

# Create your views here.
@csrf_exempt
@api_view(['GET'])
def task_list(request, st=0, en=10):
    '''
    Todo: 现在只是按task的id来索引, 实际情况下id可能会跳号等等, 而且按id会优先展示时间最靠前的
          后续修改为按照时间排序, 进一步多种排序方法
    
    用户状态: 未登录或已登录
    简介: 任务列表视图，返回任务列表
    
    params: st=start index, en=end index
    URL: /tasks/
         /tasks/task-list/
         (default st=0, en=10)
         /tasks/task-list/<int:st>/<int:en>/
    Method: GET
    Header: Content-Type: application/json, Authorization: Token token (optional)
    Body: JSON {}
    Response: 
        Success: Code 200 JSON [{'task1'}, {'task2'}, ...]
                 For each task: {
                    "id": "id",
                    "name": "name",
                    "description": "description",
                    "reward": "reward",                     (值为正整数)
                    "start_location": "start_location",     (值可以为null)
                    "end_location": "end_location",
                    "publisher": "publisher",
                    "worker": "worker",                     (可能缺失, 表示未被接受)
                    "create_time": "create_time",
                    "update_time": "update_time",
                    "deadline": "deadline",                 (时间格式均为"YYYY-MM-DDTHH:MM:SS+08:00",
                                                            例如"2024-11-12T15:05:41.480925+08:00")
                    "status": "status"                      (值为to_be_accepted, accepted, finished, out_of_date)
                 }
        Error: Code 404 JSON {'status': 'error', 'msg': 'task is not exist'}
               Code 405: Method Not Allowed
    '''
    tasks = Task.objects.all()[st:en]
    # 每次调用时检查这些任务是否过期
    for task in tasks:
        task.out_of_date()
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)
    
@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def task_detail(request, pk):
    '''
    用户状态: 未登录或已登录
    简介：任务详情视图，返回任务详情
    
    params: pk=task id
    URL: /tasks/<int:pk>/task-detail/
    Method: GET
    Header: Content-Type: application/json, Authorization: Token token (optional)
    Body: JSON {}
    Response: 
        Success: Code 200 JSON {task}
                 task介绍同上
        Error: Code 404 JSON {'status': 'error', 'msg': 'task is not exist'}
               Code 405: Method Not Allowed
    
    '''
    try:
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        return Response(status=404)
    
    if request.method == 'GET':
        serializer = TaskSerializer(task)
        return Response(serializer.data)
    else:
        return Response(status=405)
    

@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def task_create(request):
    '''
    用户状态: 已登录
    简介: 创建任务视图，接受信息并创建任务
    
    URL: /tasks/task-create/
    Method: POST
    Header: Content-Type: application/json, Authorization: Token token
    Body: JSON {
        "name": "name",
        "description": "description",
        "reward": "reward",                     (值为正整数)
        "end_location": "end_location",
        "deadline": "deadline"                  (时间格式为"YYYY-MM-DDTHH:MM:SS",
                                                例如"2024-11-12T23:05:41.480925"
                                                填写北京时间即可)
                                                
        "start_location": "start_location"      (optional)
    }
    Response:
        Success: Code 201: Created
        Error: Code 400 JSON {'status': 'error', 'msg': 'error message'}
               Code 405: Method Not Allowed
    '''
    user = request.user
    data = json.loads(request.body)
    data['publisher'] = user.id
    
    # context={'request': request} 传入request, 以便在serializer中获取user
    serializer = TaskSerializer(data=data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(status=201)
    else:
        return Response(serializer.errors, status=400)
    
@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def task_accept(request, pk):
    '''
    用户状态: 已登录
    简介: 接受任务视图, 接受特定任务
    注意: 一个用户只能接受一个任务 (暂定)
    
    params: pk=task id
    URL: /tasks/<int:pk>/task-accept/
    Method: POST
    Header: Content-Type: application/json, Authorization: Token token
    Body: JSON {}
    Response:
        Success: Code 200 JSON {'status': 'success', 'msg': 'accept success'}
        Error: Code 400 JSON {'status': 'error', 'msg': 'error message'}
               Code 405: Method Not
    
    '''
    user = request.user
    try:
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        return Response({'status': 'error', 'msg': 'task is not exist'}, status=404)
    
    try:
        # 调用task.accept()方法, 合法性检查在方法内部
        task.accept(user)
        return Response({'status': 'success', 'msg': 'accept success'})
    except Exception as e:
        return Response({'status': 'error', 'msg': str(e)}, status=400)
    
@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def task_finish(request):
    '''
    用户状态: 已登录
    简介: 完成任务视图, 完成用户当前接受的任务
    注意: 无需传入参数, 完成的是该用户当前接受的任务, 目前未检查任务完成条件
    
    URL: /tasks/task-finish/
    Method: POST
    Header: Content-Type: application/json, Authorization: Token token
    Body: JSON {}
    Response:
        Success: Code 200 JSON {'status': 'success', 'msg': 'finish success'}
        Error: Code 400 JSON {'status': 'error', 'msg': 'error message'}
               Code 405: Method Not Allowed
    '''
    
    # 选择通过当前用户的accepted_tasks来获取任务, 如果是用pk岂不是可以修改别人的任务了
    user = request.user
    try:
        # .first()是因为假定只能接受一个任务
        task = user.accepted_tasks.first()
    except Task.DoesNotExist:
        return Response({'status': 'error', 'msg': 'have not accepted task'}, status=404)
    
    try:
        task.finish()
        return Response({'status': 'success', 'msg': 'finish success'})
    except Exception as e:
        return Response({'status': 'error', 'msg': str(e)}, status=400)

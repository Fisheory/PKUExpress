from .models import Task
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status as http_status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import TaskSerializer
from .paginators import TaskPaginator

import json

# Create your views here.
class TaskList(APIView):
    '''
    URL: /tasks/
    GET方法: 列出所有任务
        参数: page = 页数 
             size = 每页个数
             search = 搜索关键字 (可选)
        
    POST方法: 创建一个新任务
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
    '''

    # 根据不同请求方法设置不同的权限
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        elif self.request.method == 'POST':
            return [IsAuthenticated()]
        return super().get_permissions()

    def get(self, request):
        paginator = TaskPaginator()
        tasks = Task.objects.all().order_by('-create_time')

        # 获取搜索参数
        search_query = request.GET.get('search')
        if search_query:
            tasks = tasks.filter(name__icontains=search_query)

        paginated_tasks = paginator.paginate_queryset(tasks, request)
        serializer = TaskSerializer(paginated_tasks, many=True)
        return Response(serializer.data)

    def post(self, request):
        # 获取当前用户并传递给序列化器
        user = request.user
        data = request.data.copy()
        data['publisher'] = user.id
        
        # 传入 request 上下文以便在序列化器中访问 user
        serializer = TaskSerializer(data=data, context={'request': request})
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=http_status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=http_status.HTTP_400_BAD_REQUEST)

class TaskDetail(APIView):
    '''
    URL: tasks/<int:pk>
    GET方法: 获取一个任务的详细信息

    PATCH方法: 更新一个任务的状态
            BODY:
            JSON {
                status: {accepted, finished}
            }
    
    DELETE方法: 删除一个任务, 仅发布者可删除
    '''

    def get_permissions(self):
        # GET 请求允许所有用户访问，PATCH, DELETE请求需要认证
        if self.request.method == 'GET':
            return [AllowAny()]
        elif self.request.method == 'PATCH':
            return [IsAuthenticated()]
        elif self.request.method == 'DELETE':
            return [IsAuthenticated()]
        return super().get_permissions()

    def get(self, request, pk):
        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response({'status': 'error', 'msg': 'Task not found'}, status=http_status.HTTP_404_NOT_FOUND)
        
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    def patch(self, request, pk):
        # 想了想还是改回纯粹的PATCH吧
        status = request.data.get('status')
        if not status:
            return Response({'status': 'error', 'msg': 'Status is required'}, status=http_status.HTTP_400_BAD_REQUEST)

        if status not in ('accepted', 'finished'):
            return Response({'status': 'error', 'msg': 'Invalid status value'}, status=http_status.HTTP_400_BAD_REQUEST)

        user = request.user
        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response({'status': 'error', 'msg': 'Task not found'}, status=http_status.HTTP_404_NOT_FOUND)

        # 根据状态进行不同操作
        try:
            if status == 'accepted':
                # 调用任务的 accept 方法，内部执行合法性检查
                task.accept(user)
                return Response({'status': 'success', 'msg': 'Task accepted successfully'})
            elif status == 'finished':
                # 检查用户是否已接受任务并完成
                if task not in user.accepted_tasks.all():
                    return Response({'status': 'error', 'msg': 'Task not accepted by this user'}, status=http_status.HTTP_403_FORBIDDEN)
                
                task.finish()
                return Response({'status': 'success', 'msg': 'Task finished successfully'})
        except Exception as e:
            return Response({'status': 'error', 'msg': str(e)}, status=http_status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, pk):
        user = request.user
        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response({'status': 'error', 'msg': 'Task not found'}, status=http_status.HTTP_404_NOT_FOUND)
        
        if task.publisher != user:
            return Response({'status': 'error', 'msg': 'Permission denied'}, status=http_status.HTTP_403_FORBIDDEN)
        
        try:
            # 现在仅状态为 to_be_accepted 的任务可以删除
            task.cancel()
            return Response({'status': 'success', 'msg': 'Task deleted successfully'})
        except Exception as e:
            return Response({'status': 'error', 'msg': str(e)}, status=http_status.HTTP_400_BAD_REQUEST)



@csrf_exempt
@api_view(['GET'])
def task_list(request):
    ''' 
    用户状态: 未登录或已登录
    简介: 任务列表视图, 返回按发布时间倒序的任务列表
    注意: 参数通过GET请求传递, 例如/tasks/task-list/?st=0&en=10
          未提供参数时默认返回前10个任务
    
    params: st=start index, (optional)
            en=end index    (optional)
    URL: /tasks/
         /tasks/task-list/
         (default st=0, en=10)
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
                    "update_time": "update_time",           (值为最后一次修改时间, 可能是状态变更)
                    "finish_time": "finish_time",           (值可能为null, 表示未完成)
                    "deadline": "deadline",                 (时间格式均为"YYYY-MM-DDTHH:MM:SS+08:00",
                                                            例如"2024-11-12T15:05:41.480925+08:00")
                    "status": "status"                      (值为to_be_accepted, accepted, finished, out_of_date)
                 }
        Error: Code 400 JSON {'status': 'error', 'msg': '...'}
               Code 405: Method Not Allowed
    '''
    st = request.GET.get('st')
    en = request.GET.get('en')
    if st is not None and en is not None:
        try:
            st = int(st)
            en = int(en)
        except ValueError:
            return Response(status=400)
    else:
        st = 0
        en = 10
    tasks = Task.objects.order_by('-create_time')[st:en]
    # 每次调用时检查这些任务是否过期
    for task in tasks:
        task.out_of_date()
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)
    
@csrf_exempt
@api_view(['GET'])
def task_detail(request):
    '''
    用户状态: 未登录或已登录
    简介: 任务详情视图, 返回特定id的任务详情
    注意: 参数通过GET请求传递, 例如/tasks/task-detail/?pk=1
    
    params: pk=task id
    URL: /tasks/task-detail/
    Method: GET
    Header: Content-Type: application/json, Authorization: Token token (optional)
    Body: JSON {}
    Response: 
        Success: Code 200 JSON {task}
                 task介绍同上
        Error: Code 400 JSON {'status': 'error', 'msg': 'error message'}
               Code 405: Method Not Allowed
    
    '''
    pk = request.GET.get('pk')
    if pk is not None:
        try:
            pk = int(pk)
        except ValueError as e:
            return Response({'status': 'error', 'msg': str(e)}, status=400)
    else:
        return Response({'status': 'error', 'msg': 'need pk'}, status=400)
    
    try:
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist as e:
        return Response({'status': 'error', 'msg': str(e)}, status=400)
    
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
        return Response(serializer.data, status=201)
    else:
        return Response(serializer.errors, status=400)
    
@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def task_accept(request):
    '''
    用户状态: 已登录
    简介: 接受任务视图, 接受特定任务
    注意: 通过POST表单传递参数, key=pk, value=task id
    
    URL: /tasks/task-accept/
    Method: POST
    Header: Content-Type: application/x-www-form-urlencoded, Authorization: Token token
    Body: key=pk, value=task id
    Response:
        Success: Code 200 JSON {'status': 'success', 'msg': 'accept success'}
        Error: Code 400 JSON {'status': 'error', 'msg': 'error message'}
               Code 405: Method Not
    
    '''
    pk = request.POST.get('pk')
    if pk is not None:
        try:
            pk = int(pk)
        except ValueError as e:
            return Response({'status': 'error', 'msg': str(e)}, status=400)
    else:
        return Response({'status': 'error', 'msg': 'need pk'}, status=400)
    
    user = request.user
    try:
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        return Response({'status': 'error', 'msg': 'task is not exist'}, status=400)
    
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
    简介: 完成任务视图, 完成用户当前接受的任务pk
    注意: 通过POST表单传递参数, key=pk, value=task id
    
    URL: /tasks/task-finish/
    Method: POST
    Header: Content-Type: application/x-www-form-urlencoded, Authorization: Token token
    Body: key=pk, value=task id
    Response:
        Success: Code 200 JSON {'status': 'success', 'msg': 'finish success'}
        Error: Code 400 JSON {'status': 'error', 'msg': 'error message'}
               Code 405: Method Not Allowed
    '''
    
    # 选择通过当前用户的accepted_tasks来获取任务, 并查询是否存在任务pk
    pk = request.POST.get('pk')
    if pk is not None:
        try:
            pk = int(pk)
        except ValueError as e:
            return Response({'status': 'error', 'msg': str(e)}, status=400)
    else:
        return Response({'status': 'error', 'msg': 'need pk'}, status=400)
    
    user = request.user
    try:
        task = user.accepted_tasks.get(pk=pk)
    except Task.DoesNotExist:
        return Response({'status': 'error', 'msg': 'have not accepted this task'}, status=400)
    
    try:
        task.finish()
        return Response({'status': 'success', 'msg': 'finish success'})
    except Exception as e:
        return Response({'status': 'error', 'msg': str(e)}, status=400)

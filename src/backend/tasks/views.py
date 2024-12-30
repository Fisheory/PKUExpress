from django.views.decorators.csrf import csrf_exempt
from rest_framework import status as http_status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import ListAPIView

from .models import Task
from .serializers import TaskSerializer
from .paginators import TaskPaginator

import json


# Create your views here.
class TaskList(APIView):
    """
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
    """

    # 根据不同请求方法设置不同的权限
    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        elif self.request.method == "POST":
            return [IsAuthenticated()]
        return super().get_permissions()

    def get(self, request):
        paginator = TaskPaginator()
        tasks = Task.objects.all().order_by("-create_time")

        for task in tasks:
            task.out_of_date()

        # 仅展示待接受的任务
        tasks = tasks.filter(status__in=["to_be_accepted"])

        # 获取搜索参数
        search_query = request.GET.get("search")
        if search_query:
            tasks = tasks.filter(name__icontains=search_query)

        paginated_tasks = paginator.paginate_queryset(tasks, request)
        serializer = TaskSerializer(paginated_tasks, many=True)
        return Response(serializer.data)

    def post(self, request):
        # 获取当前用户并传递给序列化器
        user = request.user
        data = request.data.copy()
        data["publisher"] = user.id

        # 传入 request 上下文以便在序列化器中访问 user
        serializer = TaskSerializer(data=data, context={"request": request})

        try:
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=http_status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {"msg": str(e)},
                status=http_status.HTTP_400_BAD_REQUEST,
            )


class TaskDetail(APIView):
    """
    URL: tasks/<int:pk>
    GET方法: 获取一个任务的详细信息

    PATCH方法: 更新一个任务的状态
            BODY:
            JSON {
                status: {accepted, finished}
            }

    DELETE方法: 删除一个任务, 仅发布者可删除
    """

    def get_permissions(self):
        # GET 请求允许所有用户访问，PATCH, DELETE请求需要认证
        if self.request.method == "GET":
            return [AllowAny()]
        elif self.request.method == "PATCH":
            return [IsAuthenticated()]
        elif self.request.method == "DELETE":
            return [IsAuthenticated()]
        return super().get_permissions()

    def get(self, request, pk):
        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response(
                {"msg": "Task not found"},
                status=http_status.HTTP_404_NOT_FOUND,
            )

        serializer = TaskSerializer(task)
        return Response(serializer.data)

    def patch(self, request, pk):
        # 想了想还是改回纯粹的PATCH吧
        status = request.data.get("status")
        if not status:
            return Response(
                {"msg": "Status is required"},
                status=http_status.HTTP_400_BAD_REQUEST,
            )

        if status not in ("accepted", "finished", "ack_finished"):
            return Response(
                {"msg": "Invalid status value"},
                status=http_status.HTTP_400_BAD_REQUEST,
            )

        user = request.user
        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response(
                {"msg": "Task not found"},
                status=http_status.HTTP_404_NOT_FOUND,
            )

        # 根据状态进行不同操作
        try:
            if status == "accepted":
                # 调用任务的 accept 方法，内部执行合法性检查
                task.accept(user)
                return Response({"msg": "Task accepted successfully"})
            elif status == "finished":
                # 检查用户是否已接受任务并完成
                if task not in user.accepted_tasks.all():
                    return Response(
                        {"msg": "Task not accepted by this user"},
                        status=http_status.HTTP_403_FORBIDDEN,
                    )

                task.finish()
                return Response({"msg": "Task finished successfully"})
            elif status == "ack_finished":
                if task.status != "finished":
                    return Response(
                        {"msg": "Task not finished yet"},
                        status=http_status.HTTP_400_BAD_REQUEST,
                    )
                if task not in user.published_tasks.all():
                    return Response(
                        {"msg": "Task not published by this user"},
                        status=http_status.HTTP_403_FORBIDDEN,
                    )

                task.ack_finish()
                return Response({"msg": "Task acknowledged successfully"})

        except Exception as e:
            return Response(
                {"msg": str(e)},
                status=http_status.HTTP_400_BAD_REQUEST,
            )

    def delete(self, request, pk):
        user = request.user
        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response(
                {"msg": "Task not found"},
                status=http_status.HTTP_404_NOT_FOUND,
            )

        if task.publisher != user:
            return Response(
                {"msg": "Permission denied"},
                status=http_status.HTTP_403_FORBIDDEN,
            )

        try:
            # 现在仅状态为 to_be_accepted 的任务可以删除
            task.cancel()
            return Response({"msg": "Task deleted successfully"})
        except Exception as e:
            return Response(
                {"msg": str(e)},
                status=http_status.HTTP_400_BAD_REQUEST,
            )


class UserAcceptedTaskList(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer

    def get_queryset(self):
        user = self.request.user
        return user.accepted_tasks.all().filter(status="accepted")


class UserPublishedTaskList(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer

    def get_queryset(self):
        user = self.request.user
        return user.published_tasks.all()


class UserFinishedTaskList(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer

    def get_queryset(self):
        user = self.request.user
        data = user.accepted_tasks.all().filter(status="finished")
        data |= user.accepted_tasks.all().filter(status="ack_finished")
        return data

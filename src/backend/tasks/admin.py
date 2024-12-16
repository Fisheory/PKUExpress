from django.contrib import admin
from .models import Task

<<<<<<< HEAD
# Register your models here.
class PublishedTaskInline(admin.TabularInline):
    model = Task
    fk_name = 'publisher'
    extra = 0

class AcceptedTaskInline(admin.TabularInline):
    model = Task
    fk_name = 'worker'
=======

# Register your models here.
class PublishedTaskInline(admin.TabularInline):
    model = Task
    fk_name = "publisher"
    extra = 0


class AcceptedTaskInline(admin.TabularInline):
    model = Task
    fk_name = "worker"
>>>>>>> ac4d57e3eaba250c9fdd3cb468a030d322ac2ae9
    extra = 0


class TaskAdmin(admin.ModelAdmin):
<<<<<<< HEAD
    list_display = ('name', 'description', 'reward', 'start_location', 'end_location', 'publisher',
                    'worker', 'create_time', 'update_time', 'finish_time', 'deadline', 'status')
    list_filter = ('status', 'create_time', 'update_time', 'finish_time', 'deadline')
    search_fields = ('name', 'description', 'reward', 'publisher', 'worker', 'status')
    
admin.site.register(Task, TaskAdmin)
=======
    list_display = (
        "name",
        "description",
        "reward",
        "start_location",
        "end_location",
        "publisher",
        "worker",
        "create_time",
        "update_time",
        "finish_time",
        "deadline",
        "status",
    )
    list_filter = ("status", "create_time", "update_time", "finish_time", "deadline")
    search_fields = ("name", "description", "reward", "publisher", "worker", "status")


admin.site.register(Task, TaskAdmin)
>>>>>>> ac4d57e3eaba250c9fdd3cb468a030d322ac2ae9

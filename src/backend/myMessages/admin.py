from django.contrib import admin
from .models import Message


# Register your models here.
class MessageAdmin(admin.ModelAdmin):
    list_display = ("sender", "receiver", "timestamp", "content_type", "text", "image")
    list_filter = ("timestamp", "content_type")
    search_fields = ("sender", "receiver", "content_type")


admin.site.register(Message, MessageAdmin)

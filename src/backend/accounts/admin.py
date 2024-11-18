from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin
from tasks.admin import PublishedTaskInline, AcceptedTaskInline

# Register your models here.
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        ('Personal info', {'fields': ('gold',)}),
    )
    
    list_display = ('username', 'email', 'gold', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('username', 'email')
    inlines = [PublishedTaskInline, AcceptedTaskInline]

admin.site.register(CustomUser, CustomUserAdmin)
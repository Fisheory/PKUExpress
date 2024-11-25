from django.contrib import admin
from .models import CustomUser, VerificationCode
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

class VerificationCodeAdmin(admin.ModelAdmin):
    model = VerificationCode
    list_display = ('email', 'token', 'create_time', 'usage')

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(VerificationCode, VerificationCodeAdmin)

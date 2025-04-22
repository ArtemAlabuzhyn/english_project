from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Extra fields', {'fields': ['role', 'age', 'teacher']}),
    )

    list_display = ('username', 'first_name', 'last_name', 'email', 'role', 'teacher')
    list_filter = ('role',)
    search_fields = ('username', 'first_name', 'last_name', 'email')




from django.contrib import admin
from .models import CustomUser, Profile
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email','first_name', 'last_name', 'is_staff']

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Profile)

# Register your models here.

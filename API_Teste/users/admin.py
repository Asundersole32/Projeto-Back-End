from django.contrib import admin
from models.user_model import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    list_display = [
        'uid', 
        'email', 
        'username', 
        'data_joined', 
        'last_login',
        'is_admin',
        'is_active',
        'is_staff',
        'is_superuser',
        'first_name',
        'last_name']
    list_display_links = ['uid', 'email', 'username']
    search_fields = ['uid', 'email', 'username', 'first_name', 'last_name']

admin.site.register(CustomUser, CustomUserAdmin)

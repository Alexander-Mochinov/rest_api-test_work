from django.contrib import admin
from rest_api.models import CustomUser, Operation


 
@admin.register(Operation)
class OperationAdmin(admin.ModelAdmin):
    """Пользователь"""
    list_display = ('sender', 'receiving', 'amount', 'confirmation_of_transfer')
 
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    """Пользователь"""
    list_display = ('username', 'email', 'date_joined', 'is_staff', 'user_photo', 'INN', 'amount')
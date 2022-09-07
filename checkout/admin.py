from django.contrib import admin
from .models import *


class OrderItemAdmin(admin.TabularInline):
    model = OrderItem
    extra = 1
    
    
@admin.register(Order)

class OrderAdmin(admin.ModelAdmin):
    
    list_display = ['id', 'user', 'last_name', 'total']
    
    inlines = [
        OrderItemAdmin,
    ]
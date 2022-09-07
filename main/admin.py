from django.contrib import admin
from .models import Category, Product, Detail
from django.contrib.sessions.models import Session


class SessionAdmin(admin.ModelAdmin):
    def _session_data(self, obj):
        return obj.get_decoded()
    
    list_display = [ 'session_key', '_session_data', 'expire_date']
    
admin.site.register(Session, SessionAdmin)



admin.site.register(Category)


class ProductDetailAdmin(admin.TabularInline):
    
    model = Detail
    extra = 1
    
    
@admin.register(Product)
    
class ProductAdmin(admin.ModelAdmin):
    
    save_as = True
    
    list_display = ['id', 'title', 'price', 'discount', 'is_active']
    
    list_filter = ['is_active', 'is_recommended', 'is_special', 'is_featured']
    
    list_editable = ['price', 'discount', 'is_active', 'title']
    
    inlines =  [
        ProductDetailAdmin,
    ]
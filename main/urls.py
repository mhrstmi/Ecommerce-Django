from django.urls import path
from .views import index, product_list, product_detail, search

app_name= "main"

urlpatterns = [
    path('', index, name="index"),
    path('product/list/<int:pk>/', product_list, name="product_list"),
    path('product/detail/<int:pk>/', product_detail, name="product_detail"),
    path('search/', search, name="search"),
]
from django.urls import path
from .views import *

app_name= "basket"

urlpatterns = [
    path('basket/summary/', basket_summary, name="basket_summary"),
    path('add/<int:pk>/<int:qty>/', basket_add, name="basket_add"),
    path('delete/<int:pk>/', basket_delete, name="basket_delete"),
    path('update/<int:pk>/', basket_update, name="basket_update"),
   
]
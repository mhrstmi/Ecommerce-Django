from django.urls import path
from .views import *

app_name= "checkout"

urlpatterns = [
    path('get/address/', get_address, name="get_address"),
    path('send_request/', send_request, name="send_request"),
    path('order/verify/', verify, name="verify"),
    
   
]
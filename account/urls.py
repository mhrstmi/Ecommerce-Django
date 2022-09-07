from django.urls import path
from .views import *

app_name= "account"

urlpatterns = [
    path('register/', register, name="register"),
    path('confirm/code/<pk>/<phone_number>/', confirm_code, name="confirm_code"),
    path('logout/user/', logout_user, name="logout_user"),
    path('login/user/', login_user, name="login_user"),
    path('reset/password/', reset_password, name="reset_password"),
    path('set/password/<pk>/', set_password, name="set_password"),
    path('profile/', profile, name="profile"),
    
]
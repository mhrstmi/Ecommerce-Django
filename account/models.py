from django.db import models
from django.contrib.auth.models import *


class CustomAccountManager(BaseUserManager):
    
    def create_superuser(self, phone_number, password, **other_fields):
        
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        
        if other_fields.get('is_staff') is not True:
            
            raise ValueError('Superuser must be assigned to is_staff=True.')
        
        if other_fields.get('is_superuser') is not True:
            
            raise ValueError('superuser must bet assigned to is_superuser=True')
        
        
        return self.create_user(phone_number,password, **other_fields)
    
    def create_user(self, phone_number, password, **other_fields):
        
        if not phone_number:
            raise ValueError('you must provide a phone number')
        
        user = self.model(phone_number=phone_number, **other_fields)
        
        user.set_password(password)
        user.save()
        return user
    
    
    
class Account(AbstractBaseUser, PermissionsMixin):
    
    phone_number = models.CharField(max_length=255, unique=True)
    email = models.EmailField(blank=True, null=True)
    name= models.CharField(max_length=255, blank=True)
    last_name= models.CharField(max_length=255, blank=True)
    
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    profile_img = models.ImageField(upload_to="account/profile")
    
    objects = CustomAccountManager()
    
    USERNAME_FIELD = "phone_number"
    
    def __str__(self):
        return self.phone_number
    
    
class Otp(models.Model):
    phone_number = models.CharField(max_length=255, blank=True)
    code = models.IntegerField(blank=True)
    
    def __str__(self):
        return self.phone_number
    
    
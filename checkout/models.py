from django.db import models
from account.models import Account
from main.models import Product


class Order(models.Model):
    
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="account", blank=True, null=True)
    name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    address = models.TextField()
    zipcode = models.CharField(max_length=255)
    phone_number = models.IntegerField()
    
    delivery_price = models.IntegerField()
    total = models.IntegerField()
    
    def __str__(self):
        return self.name
    

class OrderItem(models.Model):
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product")
    
    title = models.CharField(max_length=255)
    price = models.IntegerField()
    discount = models.IntegerField(blank=True, null=True)
    color = models.CharField(max_length=255, blank=True, null=True)
    size = models.CharField(max_length=255, blank=True, null=True)
    
    quantity = models.IntegerField()
    total = models.IntegerField()
    
    def __str__(self):
        return self.title
    
    
    
    
    
    
    



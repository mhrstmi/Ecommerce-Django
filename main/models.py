from django.db import models

SIZE = (
        ('S', 'S'),
        ('M', 'M'),
        ('L', 'L'),
        ('XL', 'XL'),
        ('XXL', 'XXL'),
        
    )

COLOR = (
        ('black', 'مشکی'),
        ('yellow', 'زرد'),
        ('blue', 'آبی'),
        ('red', 'قرمز')
    )


class Category(models.Model):
    title = models.CharField(max_length=255)
    
    def __str__(self):
        return self.title
    
    
    
class Product(models.Model):
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    image = models.ImageField(upload_to="product/images", blank=True)
    
    title = models.CharField(max_length=255)
    price = models.IntegerField()
    discount = models.IntegerField(blank=True, null=True)
    description = models.TextField(max_length=1000)
    amount = models.IntegerField()
    
    color = models.CharField(max_length=15, choices=COLOR, blank=True)
    size = models.CharField(max_length=15, choices=SIZE, blank=True)
    
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    is_recommended = models.BooleanField(default=False)
    is_special = models.BooleanField(default=False)
    
    def __str__(self):
        
        return self.title
    

class Detail(models.Model):
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True)
    text = models.CharField(max_length=255, blank=True)
    
    def __str__(self):
        return self.title
    
    
    
    

from django.shortcuts import render
from main.models import Product
from .basket import Basket
from django.http import HttpResponseRedirect


def basket_summary(request):
    
    products = Product.objects.filter(is_active=True).order_by('-id')
    
    context = {
        'products':products
    }
    return render(request, 'cart.html', context)



def basket_add(request, pk, qty):
    basket = Basket(request)
    
    if request.method == 'POST' :
        
        product_qty = int(request.POST.get('qty'))
        product = Product.objects.get(id=pk)
        basket.add(product=product, qty=product_qty)
        
    else:
        
        product = Product.objects.get(id=pk)
        basket.add(product=product, qty=qty)
        
    return HttpResponseRedirect(request.META.get('HTTP_REFERER') )


def basket_delete(request, pk):
    basket = Basket(request)
    
    basket.delete(product=pk)
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER') )


def basket_update(request, pk):
    basket = Basket(request)
    
    if request.method == 'POST':
        product_qty = int(request.POST.get('qty'))
        basket.update(product=pk, qty=product_qty)
        
        return HttpResponseRedirect(request.META.get('HTTP_REFERER') )
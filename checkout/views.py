from django.shortcuts import render, redirect
from basket.basket import Basket
from .models import *
from suds.client import Client

MMERCHANT_ID = "YOUR MMERCHANT_ID" 
ZARINPAL_WEBSERVICE = "https://www.zarinpal.com/pg/services/WebGate/wsdl"

description = " Door Of Time "
CallbackURL = "http://127.0.0.1:8000/checkout/order/verify/"

def get_address(request):
    
    request.session['address_info'] = {}
    
    if request.method == 'POST':
        
        name = request.POST.get('name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')
        zipcode = request.POST.get('zipcode')
        phone_number = request.POST.get('phone_number')
        
        
        request.session['address_info']['name'] = name
        request.session['address_info']['last_name'] = last_name
        request.session['address_info']['address'] = address
        request.session['address_info']['zipcode'] = zipcode
        request.session['address_info']['phone_number'] = phone_number
        
        return redirect('checkout:send_request')
    
    return render(request, 'address.html')


def send_request(request):
    
    amount = Basket(request).get_total_price()
    mobile = request.session['address_info']['phone_number']
    
    client = Client(ZARINPAL_WEBSERVICE)
    result = client.service.PaymentRequest(MMERCHANT_ID, amount, description, request.user.email, str(mobile), CallbackURL)
    
    if result.Status == 100:
        return redirect('https://www.zarinpal.com/pg/StartPay/' + str(result.Authority))
    else:
        return HttpResponse('Error' + str(result.Status))
    
    
    

def verify(request):
    
    basket = Basket(request)
    amount = basket.get_total_price()
    client = Client(ZARINPAL_WEBSERVICE)
    
    name = request.session['address_info']['name']
    last_name = request.session['address_info']['last_name']
    address = request.session['address_info']['address']
    zipcode = request.session['address_info']['zipcode']
    phone_number = request.session['address_info']['phone_number']
    
    
    if request.GET.get('Status') == 'OK':
        result = client.service.PaymentVerification(MMERCHANT_ID, request.GET['Authority'], amount)
        
        if result.Status == 100:
            
            if request.user.is_authenticated:
                
                order = Order.objects.create(
                    user = request.user,
                    name = name,
                    last_name = last_name,
                    address = address,
                    zipcode = zipcode,
                    phone_number = phone_number,
                    delivery_price = 1000,
                    total = basket.get_total_price(),
                )
                
                for obj in basket:
                    product = obj["product"]
                    
                    order_item = OrderItem.objects.create(
                        order = order,
                        product = product,
                        title = product.title,
                        price = product.price,
                        discount = product.discount,
                        color = product.color,
                        size = product.size,
                        quantity = obj['qty'],
                        total = product.price * obj['qty'],
                        
                    )
                
            else:
                
                order = Order.objects.create(
                    
                    name = name,
                    last_name = last_name,
                    address = address,
                    zipcode = zipcode,
                    phone_number = phone_number,
                    delivery_price = 1000,
                    total = basket.get_total_price(),
                )
                
                for obj in basket:
                    product = obj["product"]
                    
                    order_item = OrderItem.objects.create(
                        order = order,
                        product = product,
                        title = product.title,
                        price = product.price,
                        discount = product.discount,
                        color = product.color,
                        size = product.size,
                        quantity = obj['qty'],
                        total = product.price * obj['qty'],
                        
                    )
                    
            basket.clear()
            request.session.pop('address_info')
   
            
            return render(request, "payment-successful.html", {'order':order})
        
        
        
        elif result.Status == 101:
            if request.user.is_authenticated:
                
                order = Order.objects.create(
                    user = request.user,
                    name = name,
                    last_name = last_name,
                    address = address,
                    zipcode = zipcode,
                    phone_number = phone_number,
                    delivery_price = 1000,
                    total = basket.get_total_price(),
                )
                
                for obj in basket:
                    product = obj["product"]
                    
                    order_item = OrderItem.objects.create(
                        order = order,
                        product = product,
                        title = product.title,
                        price = product.price,
                        discount = product.discount,
                        color = product.color,
                        size = product.size,
                        quantity = obj['qty'],
                        total = product.price * obj['qty'],
                        
                    )
                
            else:
                
                order = Order.objects.create(
                    
                    name = name,
                    last_name = last_name,
                    address = address,
                    zipcode = zipcode,
                    phone_number = phone_number,
                    delivery_price = 1000,
                    total = basket.get_total_price(),
                )
                
                for obj in basket:
                    product = obj["product"]
                    
                    order_item = OrderItem.objects.create(
                        order = order,
                        product = product,
                        title = product.title,
                        price = product.price,
                        discount = product.discount,
                        color = product.color,
                        size = product.size,
                        quantity = obj['qty'],
                        total = product.price * obj['qty'],
                        
                    )
                    
            basket.clear()
            request.session.pop('address_info')
   
            
            return render(request, "payment-successful.html", {'order':order})
            
            
            
        else:
            return HttpResponse('Transaction failed. Status: ') 
    else:
        return HttpResponse('Transaction failed or canceled by user')
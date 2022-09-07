from django.shortcuts import render
from .models import Product, Category, Detail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q


def index(request):
    
    products = Product.objects.filter(is_active=True).order_by('-id')
    
    context = {
        'products':products
    }
    return render(request, 'index.html', context)


def product_list(request, pk):
    
    all_products = Product.objects.filter(is_active=True).order_by('-id')
    category = None
    
    
    if pk != 0:
        category = Category.objects.get(id=pk)
        all_products = Product.objects.filter(category=category ,is_active=True).order_by('-id')
        
    
    paginator = Paginator(all_products, 10)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
        
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    
    context = {
        'category':category,
        'products': products,
    }
    
    return render(request, 'product-list.html', context)


def product_detail(request, pk):
    
    product = Product.objects.get(id=pk)
    products = Product.objects.filter(is_active=True).order_by("-id")
    details = Detail.objects.filter(product=product)
    
    
    context = {
        'product':product,
        'products':products,
        'details':details,
    }
    return render(request, 'product-detail.html', context)
    
    
    
    
    
def search(request):
    
    all_products = Product.objects.filter(is_active=True).order_by('-id')
    searched_text = None
    results = []
    
    if request.method == 'GET':
        searched_text = request.GET.get("searched_text")
    
        results = all_products.filter(Q(title__icontains=searched_text) | Q(category__title__icontains=searched_text) | Q(id__icontains=searched_text) | Q(description__icontains=searched_text))
    
    paginator = Paginator(results, 10)
    page = request.GET.get('page')
    try:
        results = paginator.page(page)
    except PageNotAnInteger:
        results = paginator.page(1)
        
    except EmptyPage:
        results = paginator.page(paginator.num_pages)
    
    context = {
        'results': results,
        'searched_text': searched_text,
    }
    
    return render(request, 'search.html', context)
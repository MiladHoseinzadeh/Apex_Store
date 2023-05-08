from django.shortcuts import render
from ecommerce.models import Product

def indexـpage(request):
    products = Product.objects.all()[:8]
    context = {
        'products': products
    }
    return render(request, "ecommerce/index.html", context)

def shop(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, "ecommerce/shop.html", context)

def product_detail(request):
    return render(request, "ecommerce/product_detail.html")

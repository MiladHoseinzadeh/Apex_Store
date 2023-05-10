from django.db.models import Q
from django.shortcuts import render
from ecommerce.models import Product, Category

def indexـpage(request):
    products = Product.objects.all()[:8]
    context = {
        'products': products
    }
    return render(request, "ecommerce/index.html", context)

def shop(request):
    categories = Category.objects.all()
    products = Product.objects.all()

    active_category = request.GET.get('category', '')
    if active_category:
        products = products.filter(category__slug=active_category)

    query = request.GET.get('query', '')
    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))

    context = {
        'categories': categories,
        'products': products,
        'active_category': active_category,
    }
    return render(request, "ecommerce/shop.html", context)

def product_detail(request):
    return render(request, "ecommerce/product_detail.html")

import json
import stripe

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from ecommerce.models import Product, Category, Order, OrderItem
from ecommerce.cart import Cart


def indexـpage(request):
    products = Product.objects.all()[:8]
    context = {"products": products}
    return render(request, "ecommerce/index.html", context)


def shop(request):
    categories = Category.objects.all()
    products = Product.objects.all()

    active_category = request.GET.get("category", "")
    if active_category:
        products = products.filter(category__slug=active_category)

    query = request.GET.get("query", "")
    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )

    context = {
        "categories": categories,
        "products": products,
        "active_category": active_category,
    }
    return render(request, "ecommerce/shop.html", context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)

    context = {
        "product": product,
    }
    return render(request, "ecommerce/product_detail.html", context)


def show_cart(request):
    return render(request, "ecommerce/show_cart.html")


def add_to_cart(request, product_id):
    cart = Cart(request)
    cart.add(product_id)

    return render(request, "ecommerce/partials/menu_cart.html")


def update_cart(request, product_id, action):
    cart = Cart(request)

    if action == "increment":
        cart.add(product_id, 1, True)
    else:
        cart.add(product_id, -1, True)

    product = Product.objects.get(pk=product_id)
    quantity = cart.get_item(product_id)

    if quantity:
        quantity = quantity["quantity"]

        item = {
            "product": {
                "id": product.id,
                "name": product.name,
                "image": product.image,
                "get_thumbnail": product.get_thumbnail(),
                "price": product.price,
            },
            "quantity": quantity,
            "total_price": quantity * product.price,
        }
    
    else:
        item = None

    context = {
        "item": item,
    }

    response = render(request, "ecommerce/partials/cart_item.html", context)
    response["HX-Trigger"] = "update-menu-cart"

    return response


@login_required
def checkout(request):
    pub_key = settings.STRIPE_API_KEY_PUBLISHABLE
    context = {
        "pub_key": pub_key,
    }
    return render(request, "ecommerce/checkout.html", context)


def hx_menu_cart(request):
    return render(request, "ecommerce/partials/menu_cart.html")


def hx_cart_total_price(request):
    return render(request, "ecommerce/partials/cart_total_price.html")

@login_required
def place_order(request):
    cart = Cart(request)
    data = json.loads(request.body)
    total_price = 0

    items = []

    for item in cart:
        product = item["product"]
        quantity = int(item["quantity"])
        total_price += product.price * quantity

    obj = {
        "price_data": {
            "currency": "usd",
            "product_data": {
                "name": product.name
            },
            "unit_amount": product.price,
        },
        "quantity": item["quantity"]
    }

    items.append(obj)

    stripe.api_key = settings.STRIPE_API_KEY_HIDDEN
    session = stripe.checkout.Session.create(
        payment_method_types=['card',],
        line_items=items,
        mode="payment",
        success_url="http://127.0.0.1:8000/shop/cart/success/",
        cancel_url="http://127.0.0.1:8000/shop/cart/"
    )
    payment_intent = session.payment_intent

    first_name = data["first_name"]
    last_name = data["last_name"]
    email = data["email"]
    address = data["address"]
    zip_code = data["zip_code"]
    place = data["place"]
    phone = data["phone"]

    order = Order.objects.create(
        user=request.user,
        first_name=first_name,
        last_name=last_name,
        email=email,
        address=address,
        zip_code=zip_code,
        place=place,
        phone=phone,
    )
    order.payment_intent = payment_intent
    order.paid_amount = total_price
    order.paid = True
    order.save()

    for item in cart:
        product = item["product"]
        quantity = int(item["quantity"])
        price = product.price * quantity

        item = OrderItem.objects.create(
            order=order, product=product, quantity=quantity, price=price
        )

    return JsonResponse({"session": session, "order": payment_intent})

@login_required
def success_purchase(request):
    return render(request, "ecommerce/success_purchase.html")

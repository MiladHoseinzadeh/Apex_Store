from django.contrib.auth.decorators import login_required
from django.db.models import Q
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
    return render(request, "ecommerce/checkout.html")


def hx_menu_cart(request):
    return render(request, "ecommerce/partials/menu_cart.html")


def hx_cart_total_price(request):
    return render(request, "ecommerce/partials/cart_total_price.html")


def place_order(request):
    cart = Cart(request)

    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        address = request.POST.get("address")
        zip_code = request.POST.get("zip_code")
        place = request.POST.get("place")
        phone = request.POST.get("phone")

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

        for item in cart:
            product = item["product"]
            quantity = int(item["quantity"])
            price = product.price * quantity

            item = OrderItem.objects.create(
                order=order, product=product, quantity=quantity, price=price
            )

        return redirect("accounts:my_account")
    
    return redirect("ecommerce:show_cart")

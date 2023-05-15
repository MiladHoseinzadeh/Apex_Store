from ecommerce.cart import Cart

def cart(request):
    return {'cart': Cart(request)}
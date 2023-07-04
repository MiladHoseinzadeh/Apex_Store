from django.urls import path
from ecommerce.views import (
    indexـpage,
    shop,
    product_detail,
    add_to_cart,
    show_cart,
    checkout,
    hx_menu_cart,
)

app_name = "ecommerce"

urlpatterns = [
    path("", indexـpage, name="indexـpage"),
    path("shop/", shop, name="shop"),
    path("shop/cart/", show_cart, name="show_cart"),
    path("shop/cart/checkout/", checkout, name="checkout"),
    path("shop/<slug:slug>/", product_detail, name="product_detail"),
    path("shop/add_to_cart/<int:product_id>/", add_to_cart, name="add_to_cart"),
    path("hx_menu_cart/", hx_menu_cart, name="hx_menu_cart")
]

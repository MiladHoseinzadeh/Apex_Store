from django.urls import path
from ecommerce.views import (
    indexـpage,
    shop,
    product_detail,
    add_to_cart,
    show_cart,
    checkout,
    hx_menu_cart,
    update_cart,
    hx_cart_total_price,
    place_order,
    success_purchase,
)

app_name = "ecommerce"

urlpatterns = [
    path("", indexـpage, name="indexـpage"),
    path("shop/", shop, name="shop"),
    path("shop/cart/", show_cart, name="show_cart"),
    path("shop/cart/success/", success_purchase, name="success_purchase"),
    path("shop/cart/checkout/", checkout, name="checkout"),
    path("shop/<slug:slug>/", product_detail, name="product_detail"),
    path("shop/add_to_cart/<int:product_id>/", add_to_cart, name="add_to_cart"),
    path("update_cart/<int:product_id>/<str:action>/", update_cart, name="update_cart"),
    path("hx_menu_cart/", hx_menu_cart, name="hx_menu_cart"),
    path("hx_cart_total_price/", hx_cart_total_price, name="hx_cart_total_price"),
    path("place_order/", place_order, name="place_order"),

]

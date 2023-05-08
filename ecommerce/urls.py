from django.urls import path
from ecommerce.views import indexـpage, shop, product_detail

app_name = "ecommerce"

urlpatterns = [
    path("", indexـpage, name="indexـpage"),
    path("shop/", shop, name="shop"),
    path("product/", product_detail, name="product_detail"),
]

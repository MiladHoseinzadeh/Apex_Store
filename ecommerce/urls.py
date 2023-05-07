from django.urls import path
from ecommerce.views import index, shop

app_name = "ecommerce"

urlpatterns = [
    path("", index, name="index"),
    path("shop/", shop, name="shop"),
]

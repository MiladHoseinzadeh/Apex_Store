from django.contrib import admin
from ecommerce.models import Category, Product, Order, OrderItem


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "price", "created_at"]
    list_filter = ["category", "created_at"]
    search_fields = ["name", "category", "description"]


class ProductInline(admin.TabularInline):
    model = Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["title", "created_at"]
    list_filter = ["created_at"]
    search_fields = [
        "title",
    ]
    inlines = [ProductInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = [
        "order",
        "product",
        "price",
        "quantity",
        "created_at",
    ]
    list_filter = [
        "created_at",
    ]


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ["product"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "status", "created_at"]
    list_filter = ["status", "created_at"]
    search_fields = ["first_name", "last_name", "address"]
    inlines = [OrderItemInline]

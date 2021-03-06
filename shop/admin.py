from django.contrib import admin
from .models import (
    Category,
    DiscountCode,
    Order, 
    OrderItem, 
    Product,
    )
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name","slug"]
    prepopulated_fields = ({"slug":("name",)})


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name","price","category","is_available","availability","slug"]
    list_filter = ["category","is_available"]
    prepopulated_fields = ({"slug":("name",)})


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    fields = ["product","quantity","total_product_price"]
    readonly_fields = ["product","quantity","total_product_price"]
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["user","date_ordered","is_ordered","total_order_price",]
    list_filter = ["date_ordered","is_ordered","orderitems__product__name"]
    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ["user","product","quantity","total_product_price","order"]
    list_filter = ["user","product",]


@admin.register(DiscountCode)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ["code","price","is_active","date_expires"]
    list_filter = ["is_active"]
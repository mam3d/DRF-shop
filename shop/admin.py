from django.contrib import admin
from .models import Category, Order, OrderItem, Product

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    fields = ["product","quantity","total_product_price"]
    readonly_fields = ["product","quantity","total_product_price"]
    extra = 0


@admin.register(Category)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name","slug"]
    prepopulated_fields = ({"slug":("name",)})

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name","price","category","is_available","availability","slug"]
    list_editable = ["price","category","is_available","availability","slug"]
    list_filter = ["category","is_available"]
    prepopulated_fields = ({"slug":("name",)})

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["user","date_ordered","is_ordered","total_order_price"]
    list_filter = ["date_ordered","is_ordered"]
    inlines = [OrderItemInline]

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ["user","product","quantity","total_product_price","order"]
    list_filter = ["user","product",]
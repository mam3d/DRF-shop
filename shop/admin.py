from django.contrib import admin
from .models import Category, DiscountCode, Order, OrderItem, Product,Variation,VariationChoice

class VariationChoiceInline(admin.TabularInline):
    model = VariationChoice


@admin.register(Variation)
class VariationAdmin(admin.ModelAdmin):
    inlines = [VariationChoiceInline]


@admin.register(VariationChoice)
class VariationChoiceAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name","slug"]
    prepopulated_fields = ({"slug":("name",)})


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name","price","category","is_available","availability","slug"]
    list_editable = ["price","category","is_available","availability","slug"]
    list_filter = ["category","is_available"]
    prepopulated_fields = ({"slug":("name",)})


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    fields = ["product","quantity","total_product_price","variation_choices"]
    readonly_fields = ["product","quantity","total_product_price","variation_choices"]
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["user","date_ordered","is_ordered","total_order_price",]
    list_filter = ["date_ordered","is_ordered"]
    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ["user","product","quantity","total_product_price","order"]
    list_filter = ["user","product",]


@admin.register(DiscountCode)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ["code","price","is_active"]
    list_filter = ["is_active"]
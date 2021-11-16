from django.contrib import admin
from .models import Category, Order, Product

admin.site.register(Category)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name","price","category","is_available","availability","slug"]
    list_editable = ["price","category","is_available","availability","slug"]
    list_filter = ["category","is_available"]
    prepopulated_fields = ({"slug":("name",)})

@admin.register(Order)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["user","date_ordered","is_ordered"]
    list_filter = ["date_ordered","is_ordered"]
from django.contrib import admin
from .models import Category, Product

admin.site.register(Category)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name","price","category","is_available","availability","slug"]
    list_editable = ["price","category","is_available","availability","slug"]
    list_filter = ["category","is_available"]
    prepopulated_fields = ({"slug":("name",)})
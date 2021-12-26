import django_filters
from .models import Product

class ProductFilter(django_filters.FilterSet):

    class Meta:
        model = Product
        fields = {
            "category":["exact"],
            "price":["gte","lte"]
        }
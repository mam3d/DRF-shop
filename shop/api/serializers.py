from rest_framework import serializers
from shop.models import Category,Product

class CategorySerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="category",lookup_field ="slug")
    class Meta:
        model = Category
        fields = ['url',"name"]

class ProductSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="product",lookup_field ="slug")
    class Meta:
        model = Product
        fields = ['url',"name","description","price"]


class CategoryDetailSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)
    class Meta:
        model = Category
        fields = ['id',"name","products"]
from rest_framework import serializers
from shop.models import Category, OrderItem,Product,Order,DiscountCode

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

class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()
    class Meta:
        model = OrderItem
        fields = ["product","quantity","total_product_price"]

    def get_product(self,obj):
        return obj.product.name


class CartSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    orderitems = OrderItemSerializer(many=True)
    class Meta:
        model = Order
        fields = ["user","orderitems","is_ordered","total_order_price"]

    def get_user(self,obj):
        return obj.user.username

class DiscountCodeSerializer(serializers.Serializer):
    code = serializers.CharField()

    def validate(self,data):
        code = data.get("code")
        discountcode = DiscountCode.objects.filter(code=code)
        if discountcode.exists():
            discountcode = discountcode[0]
            return discountcode
        raise serializers.ValidationError("wrong code")
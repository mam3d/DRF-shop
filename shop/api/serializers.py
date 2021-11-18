
from rest_framework import serializers
from shop.models import Category, OrderItem,Product,Order,DiscountCode, VariationChoice,Variation
from django.core.validators import RegexValidator
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

class VariationChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = VariationChoice
        fields = ["id","choice"]

class VariationSerializer(serializers.ModelSerializer):
    variationchoice = serializers.SerializerMethodField()
    class Meta:
        model = Variation
        fields = ["name","variationchoice"]

    def get_variationchoice(self,obj):
        return VariationChoiceSerializer(obj.variationchoice_set.all(),many=True).data

class ProductDetailSerializer(serializers.ModelSerializer):
    variation = VariationSerializer(many=True)
    class Meta:
        model = Product
        fields = ["name","description","price","variation"]


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

from rest_framework import serializers
from shop.models import (
    Category,
    OrderItem,
    Product,
    Order,
    DiscountCode, 
    )


class CategoryListSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="category",lookup_field ="slug")
    class Meta:
        model = Category
        fields = ['url',"name"]

class ProductListSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="product",lookup_field ="slug")
    category = serializers.StringRelatedField()
    class Meta:
        model = Product
        fields = ['url',"name","description","price","category"]


class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["name","description","price"]


class CategoryDetailSerializer(serializers.ModelSerializer):
    products = ProductListSerializer(many=True)
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
    orderitems = OrderItemSerializer(many=True)
    user = serializers.StringRelatedField()
    class Meta:
        model = Order
        fields = ["user","orderitems","is_ordered","total_order_price"]
    

class DiscountCodeSerializer(serializers.Serializer):
    code = serializers.CharField()

    def validate_code(self,value):
        discountcode = DiscountCode.objects.filter(code=value)
        if discountcode.exists() and discountcode.first().is_active:
            return value
        raise serializers.ValidationError("wrong code")

    def validate(self,data):
        user = self.context["request"].user
        order_queryset = Order.objects.filter(user=user,is_ordered=False)
        if not order_queryset:
            raise serializers.ValidationError("your cart is empty")
        else:   
            order = order_queryset[0]
            if order.discount:
                raise serializers.ValidationError("you have used discount code")
            return data

    def save(self):
        discount = DiscountCode.objects.get(code=self.validated_data["code"])
        user = self.context["request"].user
        order = Order.objects.get(user=user,is_ordered=False)
        order.discount = discount.price
        order.save()


class AddProductSerializer(serializers.ModelSerializer):

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["user"].default = serializers.CurrentUserDefault()
        self.fields["user"].required = False

    class Meta:
        model = OrderItem
        fields = ["product","user"]
    
    def validate_product(self,value):
        if not value.is_available:
            raise serializers.ValidationError("this product is out of stuck")
        return value

    def create(self,validated_data):
        user = validated_data["user"]
        product = validated_data["product"]
        order,created = Order.objects.get_or_create(
            user=user,
            is_ordered = False,
            )
        orderitem,created = OrderItem.objects.get_or_create(user=user,product=product,order=order)
        if created:
            orderitem.order = order
            orderitem.save()
            return orderitem
        else:
            orderitem.quantity += 1
            orderitem.save()
            return orderitem

class RemoveProductSerializer(serializers.ModelSerializer):

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["user"].default = serializers.CurrentUserDefault()
        self.fields["user"].required = False

    class Meta:
        model = OrderItem
        fields = ["product","user"]
    
    def validate(self,data):
        orderitem = OrderItem.objects.filter(user=data["user"],product=data["product"])
        if not orderitem:
            raise serializers.ValidationError("this product isnt in your cart")
        return data

    def save(self):
        user = self.validated_data["user"]
        product = self.validated_data["product"]
        orderitem = OrderItem.objects.get(user=user,product=product)
        if orderitem.quantity == 1:
            orderitem.delete()
            return "product removed from your cart"
        else:
            orderitem.quantity -= 1
            orderitem.save()
            return "product quantity decreased"
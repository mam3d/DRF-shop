import json
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import  status
from rest_framework import generics
from shop.models import Category, Order, OrderItem, Product, VariationChoice
from .serializers import (
    CartSerializer, CategoryDetailSerializer,CategorySerializer, DiscountCodeSerializer,ProductSerializer,
    ProductDetailSerializer,
)

class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetailView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer
    lookup_field = "slug"

class ProductListView(generics.ListAPIView):
    queryset = Product.objects.filter(is_available=True)
    serializer_class = ProductSerializer

class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.filter(is_available=True)
    serializer_class = ProductDetailSerializer
    lookup_field = "slug"


class ProductAdd(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request,id):
        product = get_object_or_404(Product,id=id)
        variations = request.data.get("variations")
        variations= json.loads(variations)
        order,created = Order.objects.get_or_create(user=request.user,is_ordered=False)
        orderitemqs = OrderItem.objects.filter(user=request.user,product=product,order=order,variation_choices__id__in=variations)
        if orderitemqs.exists():
            orderitem = orderitemqs[0]
            orderitem.quantity += 1
            orderitem.save()
            return Response({"successfull":"product quantity increased"},status=status.HTTP_200_OK)
        else:
            orderitem = OrderItem.objects.create(user=request.user,product=product,order=order)
            orderitem.variation_choices.add(*variations)
            return Response({"successfull":"product add to your cart"},status=status.HTTP_200_OK)
        

class ProductRemove(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request,id):
        product = get_object_or_404(Product,id=id)
        variations = request.data.get("variations")
        variations= json.loads(variations)
        order = Order.objects.filter(user=request.user,is_ordered=False)
        if order.exists():
            order = order[0]
            orderitemqs = OrderItem.objects.filter(user=request.user,product=product,order=order,variation_choices__id__in=variations)
            if orderitemqs.exists():
                orderitem = orderitemqs.first()
                if orderitem.quantity > 1:
                    orderitem.quantity -= 1
                    orderitem.save()
                    return Response({"successfull":"your product quantity decreased"},status=status.HTTP_200_OK)
                orderitem.delete()
                return Response({"successfull":"product removed from your cart"},status=status.HTTP_200_OK)    
            else:
                return Response({"error":"this product isn't in your cart"},status=status.HTTP_400_BAD_REQUEST)
        return  Response({"error":"your cart is empty"},status=status.HTTP_400_BAD_REQUEST)



class Cart(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        orderqs = Order.objects.filter(user=request.user,is_ordered=False)
        if orderqs:
            order = orderqs[0]
            serializer = CartSerializer(order)
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response({"empty":"your cart is empty"})

class AddDiscount(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        serializer = DiscountCodeSerializer(data=request.data)
        if serializer.is_valid():
            code = serializer.validated_data
            order = Order.objects.filter(user=request.user,is_ordered=False)
            if order.exists():
                order = order[0]
                if  not order.discount:
                    order.discount = code.price
                    order.save()
                    return Response({"successfull":"discount added to your cart"},status=status.HTTP_200_OK)
                else:
                    return Response({"error":"you have already used discount code"},status=status.HTTP_400_BAD_REQUEST)
            return Response({"error":"you dont have active order"},status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
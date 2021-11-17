
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework import generics
from shop.models import Category, Order, OrderItem, Product
from .serializers import (
    CartSerializer, CategoryDetailSerializer,CategorySerializer,ProductSerializer
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
    serializer_class = ProductSerializer
    lookup_field = "slug"


class ProductAdd(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request,id):
        product = get_object_or_404(Product,id=id)
        order,created = Order.objects.get_or_create(user=request.user,is_ordered=False)
        orderitem,created = OrderItem.objects.get_or_create(user=request.user,product=product,order=order)
        if created:
            return Response({"product":product.name,"successfull":"product added to your cart"},status=status.HTTP_201_CREATED)
        else:
            orderitem.quantity += 1
            orderitem.save()
            return Response({"product":product.name,"successfull":"your product's quantity has been increased"},status=status.HTTP_201_CREATED)

class ProductRemove(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request,id):
        product = get_object_or_404(Product,id=id)
        orderitem_qs = OrderItem.objects.filter(user=request.user,product=product)
        order = Order.objects.filter(user=request.user,is_ordered=False)
        if orderitem_qs.exists():
            orderitem = orderitem_qs[0]
            if orderitem.quantity > 1:
                orderitem.quantity -= 1
                orderitem.save()
                return Response({"successfull":"your product quantity updated"},status=status.HTTP_200_OK)
            orderitem.delete()
            return Response({"successfull":"product removed from your cart"},status=status.HTTP_200_OK)

                
        else:
            return Response({"error":"this product isn't in your cart"},status=status.HTTP_400_BAD_REQUEST)



class Cart(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        orderqs = Order.objects.filter(user=request.user,is_ordered=False)
        if orderqs:
            order = orderqs[0]
            serializer = CartSerializer(order)
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response({"empty":"your cart is empty"})
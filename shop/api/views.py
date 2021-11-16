from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from shop.models import Category, Order, OrderItem, Product
from .serializers import (
    CategoryDetailSerializer,CategorySerializer,ProductSerializer
)

class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetailView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer
    lookup_field = "slug"

class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
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


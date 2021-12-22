
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404, redirect
from rest_framework.response import Response
from rest_framework import  status
from rest_framework import generics
from shop.models import Category, Order, OrderItem, Product
from .serializers import (
    CartSerializer, CategoryDetailSerializer,CategorySerializer, DiscountCodeSerializer,ProductSerializer,
    ProductDetailSerializer,
)
import requests
import json
from .permissions import CheckOutPermission

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
        order,created = Order.objects.get_or_create(user=request.user,is_ordered=False)
        if variations:
            variations= json.loads(variations)
            orderitemqs = OrderItem.objects.filter(user=request.user,product=product,order=order,variation_choices__id__in=variations)
        else:
            orderitemqs = OrderItem.objects.filter(user=request.user,product=product,order=order)
        if orderitemqs.exists():
            orderitem = orderitemqs[0]
            orderitem.quantity += 1
            orderitem.save()
            return Response({"successfull":"product quantity increased"},status=status.HTTP_200_OK)
        else:
            orderitem = OrderItem.objects.create(user=request.user,product=product,order=order)
            if variations:
                orderitem.variation_choices.add(*variations)
            return Response({"successfull":"product add to your cart"},status=status.HTTP_200_OK)
        

class ProductRemove(APIView):
    permission_classes = [IsAuthenticated,]

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
        return Response({"empty":"your cart is empty"},status=status.HTTP_400_BAD_REQUEST)

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



class CheckoutView(APIView):
    permission_classes = [IsAuthenticated,CheckOutPermission]

    def post(self,request):
        headers = {"X-API-KEY":"c7eb1f53-22cb-4f6c-a8a9-fe18439e44a4","X-SANDBOX":"true"}
        user = request.user
        order = Order.objects.get(user=user,is_ordered=False)
        data = {
            "order_id": order.id,
            "amount":order.total_order_price,
            "phone":user.phone,
            "callback":"http://127.0.0.1:8000/api/verify/"
        }
        response = requests.post("https://api.idpay.ir/v1.1/payment",json=data,headers=headers)
        dic = json.loads(response.content)
        order.idpay_code = dic["id"]
        order.save()
        return redirect(str(dic["link"]))

class VerifyView(APIView):
    permission_classes = [IsAuthenticated,CheckOutPermission]

    def post(self,request):
        if int(request.POST["status"]) == 10:
            order_id = request.POST["order_id"]
            id = request.POST["id"]
            order = Order.objects.get(id=order_id)
            order.idpay_track_id = request.POST["track_id"]
            order.save()
            if id == order.idpay_code and order.idpay_track_id == request.POST["track_id"]:
                order.is_ordered = True
                order.save()
                return Response({"success":"thanks","order_id":order_id,"track_id":request.POST["track_id"]},status=status.HTTP_201_CREATED)
            return Response({"error":"something went wrong"},status=status.HTTP_400_BAD_REQUEST)
        elif int(request.POST["status"]) == 2:
            return Response({"refunded":"payment was unsucessfull"})
            

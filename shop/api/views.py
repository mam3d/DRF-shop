from django.core.cache import cache
from django.shortcuts import get_object_or_404
from django.http import Http404
from rest_framework import (
        views,
        permissions,
        response,
        generics,
        status
        )
from shop.models import (
    Category, 
    Order, 
    Product
    )
from .serializers import (
    CartSerializer,
    CategoryDetailSerializer,
    CategoryListSerializer, 
    DiscountCodeSerializer,
    ProductListSerializer,
    ProductDetailSerializer,
    AddProductSerializer,
    RemoveProductSerializer
    )
from ..helpers import pay_with_idpay
from .permissions import (
    CheckOutPermission,
    UserInfoPermission,
    )
from user.models import (
        UserOrder
        )

class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer


class CategoryDetailView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer
    lookup_field = "slug"


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.filter(is_available=True)
    serializer_class = ProductListSerializer


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.filter(is_available=True)
    serializer_class = ProductDetailSerializer
    lookup_field = "slug"


class AddProductToCart(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AddProductSerializer
    
    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return response.Response("item added to your cart",status=status.HTTP_201_CREATED)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["request"] = self.request
        return context


class RemoveProductFromCart(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = RemoveProductSerializer(data=request.data, context={"request":request})
        serializer.is_valid(raise_exception=True)
        response_message = serializer.save()
        return response.Response(response_message)
    

class Cart(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        queryset = Order.objects.filter(user=request.user,is_ordered=False)
        if queryset:
            serializer = CartSerializer(queryset[0])
            return response.Response(serializer.data)
        return response.Response("your cart is empty",status=status.HTTP_403_FORBIDDEN)


class AddDiscount(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self,request):
        serializer = DiscountCodeSerializer(data=request.data,context={"request":request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response("added discount code")


class CheckoutView(views.APIView):
    permission_classes = [
        permissions.IsAuthenticated,
        CheckOutPermission,
        UserInfoPermission
        ]
    def post(self, request):
        user = request.user
        response = pay_with_idpay(user)
        cache.set(f"{user.phone}_idpay", response["id"])
        return response.Response(response["link"])

    def get(self, request):
        idpay_id_in_cache = cache.get(f"{request.user.phone}_idpay")
        idpay_id = request.GET.get("id")
        if idpay_id is None:
            raise Http404

        if int(request.GET.get("status")) == 10 and idpay_id_in_cache == idpay_id:

            order_id = request.GET.get("order_id")
            order = Order.objects.get(id=order_id)
            order.is_ordered = True
            order.save()
            
            for orderitems in order.orderitems.all():
                product = orderitems.product
                product.availability -= orderitems.quantity
                product.save()

            UserOrder.objects.create(
                    user = request.user,
                    track_id = request.GET.get("track_id"),
                    order = order,
                    )
            cache.delete(f"{request.user.phone}_idpay")
            return response.Response("thanks for your purchase")
        cache.delete(f"{request.user.phone}_idpay")
        return response.Response("purchase failed")

            

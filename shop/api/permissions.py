from rest_framework.permissions import BasePermission
from shop.models import Order

class CheckOutPermission(BasePermission):
    message = "you must have products in your cart in order to preceed to checkout"
    def has_permission(self, request, view):
        user = request.user
        order = Order.objects.filter(user=user,is_ordered=False)
        if order.exists():
            order = order[0]
            orderitems = order.orderitems.all()
            return bool(orderitems.exists())
        return False

class UserInfoPermission(BasePermission):
    message = "you must complete your info (address and postal code)"
    def has_permission(self, request, view):
        user = request.user
        return bool(user.address and user.postal_code)
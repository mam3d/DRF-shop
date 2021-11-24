from rest_framework.permissions import BasePermission
from shop.models import Order

class CheckOutPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        order = Order.objects.filter(user=user,is_ordered=False)
        if order.exists():
            order = order[0]
            orderitems = order.orderitems.all()
            return bool(orderitems.exists() and user.postal_code and user.address)
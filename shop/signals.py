from django.db.models.signals import post_delete
from .models import OrderItem,Order

def order_delete(sender,instance,using,**kwargs):
    order = instance.order
    orderitems = order.orderitem_set.all()
    if not orderitems:
        order.delete()

post_delete.connect(order_delete,OrderItem)
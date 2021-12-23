from django.utils import timezone
from celery import shared_task
from .models import DiscountCode

@shared_task(ignore_result=True)
def delete_discount():
    discount = DiscountCode.objects.filter(date_expires__lt=timezone.now())
    if discount:
        discount.delete()

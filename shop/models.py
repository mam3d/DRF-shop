from django.db import models
from django.conf import settings
from django.template.defaultfilters import slugify

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    def __str__(self):
        return self.name

    def save(self,*args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        
        return super().save(*args, **kwargs)
    class Meta:
        verbose_name_plural = "categories"


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True,null=True)
    image = models.ImageField(blank=True,null=True)
    price = models.PositiveIntegerField()
    category = models.ForeignKey(Category,on_delete=models.SET_NULL,blank=True,null=True)
    is_available = models.BooleanField(default=True)
    availability = models.IntegerField()
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name
    

    def save(self,*args, **kwargs):
        if self.availability < 1:
            self.is_available = False
        if not self.slug:
            self.slug = slugify(self.name)
        
        return super().save(*args, **kwargs)


class Order(models.Model):
    user  = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    is_ordered = models.BooleanField(default=False)
    date_ordered = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}'s order"

    def total_order_price(self):
        total = 0
        for order in self.orderitem_set.all():
            total += order.total_product_price

        return total
class OrderItem(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    user  = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    order = models.ForeignKey(Order,on_delete=models.CASCADE)

    @property
    def total_product_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.user}'s orderitem"
from django.test import  TestCase
from shop.models import Category, Order, OrderItem, Product
from django.contrib.auth import get_user_model
class CategoryTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="test 123")
    

    def test_model(self):
        self.assertEqual(self.category.name,"test 123")
        self.assertEqual(self.category.slug,"test-123")
        self.assertEqual(str(self.category),"test 123")

class ProductTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name="ps5",
            price = 120,
            is_available = True,
            availability = 2,
        )
    

    def test_model(self):
        self.assertEqual(self.product.name,"ps5")
        self.assertEqual(self.product.price,120)
        self.assertEqual(str(self.product),"ps5")
        self.assertFalse(self.product.description)
        self.assertFalse(self.product.image)
        self.assertFalse(self.product.category)
        self.assertTrue(self.product.is_available)
        self.product.availability = 0
        self.product.save()
        self.assertFalse(self.product.is_available)

class OrderItemTest(TestCase):
    def setUp(self):
        product = Product.objects.create(
            name="ps5",
            price = 120,
            is_available = True,
            availability = 2,
        )
        user = get_user_model().objects.create_user(phone="09026673395",password="testing321")
        order = Order.objects.create(user=user)
        self.orderitem = OrderItem.objects.create(
            product = product,
            user = user,
            order = order,
            quantity = 2
        )
    

    def test_model(self):
        self.assertEqual(self.orderitem.product.name,"ps5")
        self.assertEqual(self.orderitem.user.phone,"09026673395")
        self.assertEqual(str(self.orderitem),"09026673395's orderitem")
        self.assertEqual(self.orderitem.total_product_price,240)


class OrderTest(TestCase):
    def setUp(self):
        product = Product.objects.create(
            name="ps5",
            price = 100,
            is_available = True,
            availability = 2,
        )
        user = get_user_model().objects.create_user(phone="09026673395",password="testing321")
        self.order = Order.objects.create(user=user)
        orderitem1 = OrderItem.objects.create(
            product = product,
            user = user,
            order = self.order,
            quantity = 2
        )
        orderitem2 = OrderItem.objects.create(
            product = product,
            user = user,
            order = self.order,
            quantity = 1
        )
        

    def test_model(self):
        self.assertEqual(self.order.user.phone,"09026673395")
        self.assertFalse(self.order.is_ordered)
        self.assertEqual(str(self.order),"09026673395's order")
        self.assertEqual(self.order.total_order_price,300)

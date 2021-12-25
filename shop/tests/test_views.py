from django.utils import timezone
from rest_framework.test import APITestCase
from json import dumps
from django.urls import reverse
from shop.models import (
        Category,
        Order,
        Product,
        OrderItem,
        DiscountCode
        )
from user.models import CustomUser
from knox.models import AuthToken

class CategoryListViewTest(APITestCase):
    def setUp(self):
        self.url = reverse("categories")
        Category.objects.create(name="test")

    def test_response(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code,200)


class CategoryDetailViewTest(APITestCase):
    def setUp(self):
        self.url = reverse("category",kwargs={"slug":"test"})
        Category.objects.create(name="test")

    def test_response(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code,200)


class ProductListViewTest(APITestCase):
    def setUp(self):
        self.url = reverse("products")
        Product.objects.create(name="test",price=100,availability=10)

    def test_response(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code,200)


class ProductDetailViewTest(APITestCase):
    def setUp(self):
        self.url = reverse("product",kwargs={"slug":"test"})
        Product.objects.create(name="test",price=100,availability=10)

    def test_response(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code,200)


class AddProductToCardViewTest(APITestCase):
    def setUp(self):
        self.url = reverse("cart_add")
        self.product = Product.objects.create(name="test",price=100,availability=10)
        self.user = CustomUser.objects.create_user(phone="9006673395",password="testing321")
        self.token = AuthToken.objects.create(user=self.user)

    def test_product_added(self):
        data = {
            "product": self.product.id
        }
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token[1]}")
        response = self.client.post(self.url, data=data, format="json")
        order = Order.objects.get(user=self.user,is_ordered=False)
        self.assertTrue(order)
        self.assertEqual(response.status_code,201)

    def test_product_permission(self):
        data = {
            "product": self.product.id
        }
        response = self.client.post(self.url,data=data, format="json")
        self.assertEqual(response.status_code,401)


class RemoveProductFromCartViewTest(APITestCase):
    def setUp(self):
        self.url = reverse("cart_remove")
        self.product = Product.objects.create(name="test",price=100,availability=10)
        self.user = CustomUser.objects.create_user(phone="9006673395",password="testing321")
        self.token = AuthToken.objects.create(user=self.user)
        order = Order.objects.create(user=self.user,is_ordered=False)
        self.order_item = OrderItem.objects.create(
            user = self.user,
            product = self.product,
            quantity = 2,
            order = order
            )

    def test_product_removed(self):
        data = {
            "product": self.product.id
        }
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token[1]}")
        response = self.client.post(self.url, data=data, format="json")
        order_item = OrderItem.objects.get(user=self.user)

        self.assertEqual(order_item.quantity,1)
        self.assertEqual(response.status_code,200)

    def test_product_remove_permission(self):
        data = {
            "product": self.product.id
        }
        response = self.client.post(self.url, data=data, format="json")
        self.assertEqual(response.status_code, 401)


class CartViewTest(APITestCase):
    def setUp(self):
        self.url = reverse("cart")
        self.user = CustomUser.objects.create_user(phone="9006673395",password="testing321")
        self.token = AuthToken.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token[1]}")

    def test_response(self):
        Order.objects.create(user=self.user,is_ordered=False)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code,200)

    def test_permission_denied(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code,403)


class AddDiscountTest(APITestCase):
    def setUp(self):
        self.url = reverse("add_discount")
        self.user = CustomUser.objects.create_user(phone="9006673395",password="testing321")
        self.token = AuthToken.objects.create(user=self.user)
        product = Product.objects.create(name="test",price=200,availability=10)
        order = Order.objects.create(user=self.user,is_ordered=False)
        OrderItem.objects.create(
            user = self.user,
            product = product,
            quantity = 1,
            order = order
            )
        DiscountCode.objects.create(code="test",price=100,date_expires=timezone.now(),is_active=True)

    def test_response(self):
        data = {
            "code":"test"
        }
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token[1]}")
        response = self.client.post(self.url, data=data, format="json")
        order = Order.objects.get(user=self.user,is_ordered=False)
        self.assertEqual(order.total_order_price,100) # 200 - 100
        self.assertEqual(response.status_code,200)

    def test_unauthenticated(self):
        data = {
            "code":"test"
        }
        response = self.client.post(self.url, data=data, format="json")
        self.assertEqual(response.status_code, 401)
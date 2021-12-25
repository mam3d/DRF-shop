from rest_framework.test import APITestCase
from django.urls import reverse
from knox.models import AuthToken
from ..models import (
    PhoneOtp,
    CustomUser
    )


class PhoneVerifyCreateTest(APITestCase):
    def setUp(self):
        self.url = reverse("validate_phone")

    def test_create(self):
        data = {
            "phone":"09026673395"
        }
        response = self.client.post(self.url, data=data, format="json")
        self.assertEqual(response.status_code,201)

    def test_not_create(self):
        data = {
            "phone":"09026asfa673395"
        }
        response = self.client.post(self.url, data=data, format="json")
        self.assertEqual(response.status_code,400)

    def test_phone_queryset_exists(self):
        PhoneOtp.objects.create(
            phone = "09036673395",
            code = 45656,
            count = 1
            )
        data = {
            "phone":"09036673395"
        }
        response = self.client.post(self.url, data=data, format="json")
        phone = PhoneOtp.objects.get(phone="09036673395")
        self.assertEqual(phone.count,2)
        self.assertEqual(response.status_code,201)


class UserRegisterViewTest(APITestCase):
    def setUp(self):
        self.url = reverse("register")
        self.phone = PhoneOtp.objects.create(
                        phone = "09026673395",
                        code = 123456,
                        )

    def test_create(self):
        data = {
            "phone":"09026673395",
            "password":"imtestingit",
            "password2":"imtestingit",
            "code":123456.
        }
        response = self.client.post(self.url, data=data, format="json")
        self.assertEqual(response.status_code,201)

    def test_not_create(self):
        data = {
            "phone":"09026asfa673395",
            "password":"imtestingit",
            "password2":"oafasflkafsf",
            "code":00000,
        }
        response = self.client.post(self.url, data=data, format="json")
        self.assertEqual(response.status_code,400)

class UserInfoViewTest(APITestCase):

    def setUp(self):
        self.url = reverse("user-info")
        self.user = CustomUser.objects.create_user(
            phone = "09006673391",
            password = "testing321"
        )
        self.token = AuthToken.objects.create(user=self.user)

    def test_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token[1]}")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code,200)

    def test_unauthenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code,401)

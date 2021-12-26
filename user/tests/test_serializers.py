from django.core.cache import cache
from user.api.serializers import (
    PhoneVerifySerializer,
    UserRegisterSerializer,
    LoginSerializer,
    UserInfoSerializer
    )
from django.test import TestCase
from user.models import CustomUser


class PhoneSerializerTest(TestCase):

    def test_serializer_isvalid(self):
        serializer = PhoneVerifySerializer(data={"phone":"09036673395"})
        self.assertTrue(serializer.is_valid())

    def test_serializer_notvalid(self):
        serializer = PhoneVerifySerializer(data={"phone":"0902667safs3395"})
        self.assertFalse(serializer.is_valid())


class UserRegisterSerializerTest(TestCase):
    
    def test_is_valid(self):
        cache.set("09026673395", 1243)
        data = {
            "phone":"09026673395",
            "password":"testing321",
            "password2":"testing321",
            "code":1243
        }
        serializer =  UserRegisterSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_not_valid(self):
        data = {
            "phone":"09026673395xx",
            "password":"testing321",
            "password2":"testing321"
        }
        serializer =  UserRegisterSerializer(data=data)
        data2 = {
            "phone":"09026673395",
            "password":"testing321",
            "password2":"testing321"
        }


        serializer2 =  UserRegisterSerializer(data=data2)
        self.assertFalse(serializer.is_valid())
        self.assertFalse(serializer2.is_valid())


class LoginSerializerTest(TestCase):
    def test_is_valid(self):
        user = CustomUser.objects.create_user(phone="09026673395",password="testing321")
        data = {
            "phone":"09026673395",
            "password":"testing321",
        }
        serializer =  LoginSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_not_valid(self):
        user = CustomUser.objects.create_user(phone="09026673395",password="testing321")
        data = {
            "phone":"09026673395",
            "password":"",
        }
        serializer =  LoginSerializer(data=data)
        self.assertFalse(serializer.is_valid())


class   UserInfoSerializerTest(TestCase):
    def test_is_valid(self):
        user = CustomUser.objects.create_user(phone="09026673395",password="testing321")
        data = {
            "name":"sss",
            "address":"test",
            "postal_code": 1236
        }
        serializer =  UserInfoSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_not_valid(self):
        user = CustomUser.objects.create_user(phone="09026673395",password="testing321")
        data = {
            "name":1234,
            "address":4554,
            "postal_code": "ss"
        }
        serializer =  UserInfoSerializer(data=data)
        self.assertFalse(serializer.is_valid())


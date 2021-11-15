from user.api.serializers import PhoneSerializer,UserRegisterSerializer,LoginSerializer
from django.test import TestCase
from user.models import CustomUser, PhoneOtp


class PhoneSerializerTest(TestCase):

    def test_serializer_isvalid(self):
        serializer = PhoneSerializer(data={"phone":"09036673395"})
        self.assertTrue(serializer.is_valid())

    def test_serializer_notvalid(self):
        serializer = PhoneSerializer(data={"phone":"0902667safs3395"})
        self.assertFalse(serializer.is_valid())


class UserRegisterSerializerTest(TestCase):
    
    def test_is_valid(self):
        phoneotp = PhoneOtp.objects.create(phone="09026673395",code=1243)
        data = {
            "phone":"09026673395",
            "password":"testing321",
            "password2":"testing321"
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
        phoneotp = PhoneOtp.objects.create(phone="0912792556",code=1243)
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


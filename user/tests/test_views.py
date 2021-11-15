from django.test import TestCase
from django.urls import reverse
from rest_framework import response
from user.api.serializers import PhoneSerializer,UserRegisterSerializer
from user.models import CustomUser, PhoneOtp

class ValidatePhoneViewTest(TestCase):
    def setUp(self):
        self.url = reverse("validate-phone")
        
    def test_phone_already_registerd(self):
        user = CustomUser.objects.create(phone="09036673395")
        response = self.client.post(self.url,{"phone":"09036673395"})
        self.assertEqual(response.status_code,400)

    def test_phoneotp_created(self):
        response = self.client.post(self.url,{"phone":"09036673395"})
        phone_otp = PhoneOtp.objects.get(phone="09036673395")
        self.assertTrue(phone_otp)

    def test_phoneotp_limit(self):
        phone_otp = PhoneOtp.objects.create(phone="09026673395",counter=9,code=120313)
        response = self.client.post(self.url,{"phone":"09026673395"})
        self.assertEqual(response.status_code,400)

    def test_sms_sent_phoneotp_exists(self):
        phone_otp = PhoneOtp.objects.create(phone="09026673395",counter=1,code=120313)
        response = self.client.post(self.url,{"phone":"09026673395"})
        self.assertEqual(response.status_code,200)

    def tests_sms_sent_phoneotp_notexists(self):
        response = self.client.post(self.url,{"phone":"09026674395"})
        self.assertEqual(response.status_code,200)



class RegisterViewTest(TestCase):

    def setUp(self):
        self.url = reverse("register")

    def test_user_created(self):
        phoneotp = PhoneOtp.objects.create(phone="09026673395",code=1234)
        response = self.client.post(self.url,data={"phone":"09026673395","password":"testing321","password2":"testing321","code":1234})
        self.assertEqual(response.status_code,201)

    def test_user_not_created(self):
        phoneotp = PhoneOtp.objects.create(phone="09126673395",code=1234)
        response = self.client.post(self.url,data={"phone":"09026673395","password":"testing321","password2":"testing321","code":1234})
        self.assertEqual(response.status_code,400)


class LoginViewTest(TestCase):

    def setUp(self):
        self.url = reverse("login")
    
    def test_user_can_log_in(self):
        CustomUser.objects.create(phone="09026673395",password="testing321")
        response = self.client.post({"phone":"09026673395","password":"testing321"})
        self.assertEqual(response.status_code,200)

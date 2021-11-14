from django.test import TestCase
from django.urls import reverse
from user.api.serializers import PhoneSerializer
from user.models import CustomUser, PhoneOtp

class ValidatePhoneViewTest(TestCase):
    def setUp(self):
        self.url = reverse("validate-phone")

    def test_serializer_isvalid(self):
        serializer = PhoneSerializer(data={"phone":"09036673395"})
        self.assertTrue(serializer.is_valid())

    def test_serializer_notvalid(self):
        serializer = PhoneSerializer(data={"phone":"0902667safs3395"})
        self.assertFalse(serializer.is_valid())
        
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
        response = self.client.post(self.url,{"phone":"09026673395"})
        self.assertEqual(response.status_code,200)

from django.test import TestCase
from user.models import (
    CustomUser,
    PhoneOtp,
    )

class CustomUserModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(phone="09358733401",password="testing321")

    def test_user_exists(self):
        self.assertEqual(self.user.phone,"09358733401")
        self.assertTrue(self.user.check_password("testing321"))
        self.assertEqual(self.user.name,None)
        self.assertEqual(self.user.address,None)
        self.assertEqual(self.user.postal_code,None)
        self.assertEqual(str(self.user),"09358733401")
    


class CustomUserModelTest(TestCase):
    def setUp(self):
        self.phoneotp = PhoneOtp.objects.create(
            phone = "09358733401",
            code = 1012,
            count = 1,
            )

    def test_phoneotp_created(self):
        self.assertEqual(self.phoneotp.phone,"09358733401")
        self.assertEqual(self.phoneotp.code,1012)
        self.assertEqual(self.phoneotp.count,1)
        self.assertEqual(str(self.phoneotp),"09358733401's otp")
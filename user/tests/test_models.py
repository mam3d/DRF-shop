from django.test import TestCase
from user.models import CustomUser

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
    
    def test_user_correct_format(self):
        user = CustomUser.objects.create_user(phone="358733401",password="testing321")
        self.assertRaises(ValueError)
from django.test import TestCase
from django.core.exceptions import ValidationError
from ..validators import (
            phone_validator,
            )


class PhoneValidatorTest(TestCase):

    def test_raise(self):
        with self.assertRaises(ValidationError):
            phone_validator("092asasa02asg5")
    
    def test_returend_data(self):
        phone = phone_validator("09026673395")
        self.assertEqual(phone,"09026673395")


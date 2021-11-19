
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
from django.core.validators import RegexValidator

regex = RegexValidator(r'09\d{9}',"please enter correct format ex:0912***2027")

class UserManager(BaseUserManager):
    def create_user(self,phone,password):
        if not phone:
            raise ValueError("you must enter phone number")
        else:
            user = self.model(phone=phone)
            user.set_password(password)
            user.save()
            return user

    def create_superuser(self,phone,password):
        user = self.create_user(phone=phone,password=password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class CustomUser(AbstractBaseUser,PermissionsMixin):
    phone = models.CharField(max_length=11,unique=True,validators=[regex])
    name = models.CharField(max_length=100,blank=True,null=True)
    address = models.CharField(max_length=100,blank=True,null=True)
    postal_code = models.IntegerField(blank=True,null=True)
    date_joined  = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    objects = UserManager()


    USERNAME_FIELD = "phone"

    
    def __str__(self):
        if self.name:
            return self.name
        return str(self.phone)


class PhoneOtp(models.Model):
    phone = models.CharField(max_length=11,validators=[regex])
    code = models.IntegerField()
    verfied = models.BooleanField(default=False)
    counter = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.phone}'s otp"
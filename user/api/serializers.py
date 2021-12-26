import random
from django.core.cache import cache
from django.contrib.auth import authenticate
from rest_framework import serializers
from ..models import (
        CustomUser,
        )
from ..validators import (
        phone_validator,
        check_user_not_exists,
        )

class PhoneVerifySerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=11, validators=[phone_validator, check_user_not_exists])
    code = serializers.IntegerField(default=random.randint(9999,99999))
        
class UserRegisterSerializer(serializers.ModelSerializer):
    code = serializers.IntegerField()
    password2 = serializers.CharField()
    class Meta:
        model = CustomUser
        fields = ["phone","password","password2","code"]

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["phone"].validators.extend([phone_validator])

    def validate_phone(self,value):
        phoneotp = cache.get(value)
        if phoneotp is None:
            raise serializers.ValidationError("you must verify your phone first")
        return value

        
    def validate(self,data):
        phone = data.get("phone")
        password = data.get("password")
        password2 = data.get("password2")
        code = data.get("code")
        phoneotp_code = cache.get(phone)
        
        if password != password2:
            raise serializers.ValidationError("passwords didnt match!")
        elif code != phoneotp_code:
            raise serializers.ValidationError("wrong code")
        return data

    def save(self):
        phone = self.validated_data["phone"]
        password = self.validated_data["password"]
        user = CustomUser.objects.create_user(
            phone = phone,
            password = password
        )
        cache.delete(phone)
        return user


class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField(validators=[phone_validator])
    password = serializers.CharField()

    def validate(self,data):
        phone = data.get("phone")
        password = data.get("password")
        user = authenticate(username=phone,password=password)
        if user is None:
            raise serializers.ValidationError("phone number or password is inccorect")
        return user

class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["name","phone","address","postal_code"]
        extra_kwargs = {
            "phone":{"read_only":True}
        }
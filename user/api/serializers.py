from rest_framework import serializers
from django.contrib.auth import authenticate
from ..models import (
        CustomUser,
        PhoneOtp
        )
from ..validators import (
        phone_validator,
        check_user_not_exists,
        )

class PhoneVerifySerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneOtp
        fields = ["phone"]

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["phone"].validators.extend([phone_validator,check_user_not_exists])
    
    def validate_phone(self,value):
        phone_queryset = PhoneOtp.objects.filter(phone=value)
        if phone_queryset.exists():
            phone_verify = phone_queryset.first()
            if phone_verify.count >= 8:
                raise serializers.ValidationError("you cant request code anymore")
            return value
        return value

        
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
        phone_queryset = PhoneOtp.objects.filter(phone=value)
        if not phone_queryset:
            raise serializers.ValidationError("you must verify your phone first")
        return value

        
    def validate(self,data):
        phone = data.get("phone")
        password = data.get("password")
        password2 = data.get("password2")
        code = data.get("code")
        phone_verify = PhoneOtp.objects.get(phone=phone)
        if password != password2:
            raise serializers.ValidationError("passwords didnt match!")
        elif code != phone_verify.code:
            raise serializers.ValidationError("wrong code")
        return data

    def save(self):
        user = CustomUser.objects.create_user(
            phone = self.validated_data["phone"],
            password = self.validated_data["password"]
        )
        phone = PhoneOtp.objects.get(phone=self.validated_data["phone"])
        phone.delete()
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
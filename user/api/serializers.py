from rest_framework import serializers
from ..models import CustomUser, PhoneOtp
from django.core.validators import RegexValidator
import re
def length_validator(value):
    if len(value) < 8:
        raise serializers.ValidationError("you must enter at least 8 characters")
    return value

def regex_validator(value):
        if re.match(r'09\d{9}$',value):
            return value
        raise serializers.ValidationError("please enter correct format ex:0912***2027")




class UserRegisterSerializer(serializers.Serializer):
    phone = serializers.CharField(validators=[regex_validator])
    password = serializers.CharField(validators=[length_validator])
    password2 = serializers.CharField(validators=[length_validator])

    def validate_phone(self,value):
        user = CustomUser.objects.filter(phone=value)
        if user.exists():
            raise serializers.ValidationError("this phone number already taken")
        return value

    def validate(self,data):
        password = data.get("password")
        password2 = data.get("password2")
        phoneotp = PhoneOtp.objects.filter(phone=data.get("phone"))
        if password != password2:
            raise serializers.ValidationError("password's didn't match",code="Not matched")
        if not phoneotp:
            raise serializers.ValidationError("you must verify your number first",code="not verified")
        else:
            return data
        

    def create(self,validated_data):
        user = CustomUser(phone=validated_data.get("phone"))
        user.set_password(validated_data.get("password"))
        user.save()
        return user



class PhoneSerializer(serializers.Serializer):
    phone = serializers.CharField(validators=[regex_validator])


    def validate_phone(self,value):
        user = CustomUser.objects.filter(phone=value)
        if user.exists():
            raise serializers.ValidationError("this phone number already taken")
        return value
        
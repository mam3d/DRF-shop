from rest_framework import serializers
from ..models import CustomUser
from django.core.validators import RegexValidator
import re
def length_validator(value):
    if len(value) < 8:
        raise serializers.ValidationError("you must enter at least 8 characters")
    return value

class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(validators=[length_validator])

    class Meta:
        model = CustomUser
        fields = ["phone","password","password2"]

    def validate_phone(self,value):
        user = CustomUser.objects.get(phone=value)
        if user:
            raise serializers.ValidationError("this phone number already taken")
        return value

    def validate(self,data):
        password = data.get("password")
        password2 = data.get("password2")
        if password != password2:
            raise serializers.ValidationError("password's didn't match",code="Not matched")
        return data

    def create(self,validated_data):
        user = CustomUser(phone=validated_data.get("phone"))
        user.set_password(validated_data.get("password"))
        user.save()
        return user



class PhoneSerializer(serializers.Serializer):
    def regex_validator(value):
        if re.match(r'09\d{9}$',value):
            return value
        raise serializers.ValidationError("please enter correct format ex:0912***2027")
    phone = serializers.CharField(validators=[regex_validator])


    def validate_phone(self,value):
        user = CustomUser.objects.get(phone=value)
        if user:
            raise serializers.ValidationError("this phone number already taken")
        return value
        
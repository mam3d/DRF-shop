
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import  status
from django.shortcuts import get_object_or_404
from ..models import CustomUser, PhoneOtp
import random
from .serializers import PhoneSerializer, UserRegisterSerializer, LoginSerializer,UserInfoSerializer
from kavenegar import *
from knox.models import AuthToken



def send_sms(code,phone):
    api = KavenegarAPI('')
    params = { 
        'receptor': phone,
        'message' :f"""
                            سلام کد ورود شما جهت اعتبار سنجی

                            {code}
        """}
    response = api.sms_send( params)

class ValidatePhone(APIView):
    def post(self,request):
        serializer = PhoneSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data.get("phone")
            otp_qs = PhoneOtp.objects.filter(phone=phone)
            if otp_qs.exists():
                otp = otp_qs[0]
                if otp.counter > 8:
                    return Response(
                        {"error":"you cant request code anymore"},
                        status=status.HTTP_400_BAD_REQUEST)

                        
                otp.code = random.randint(9999,99999)
                otp.counter += 1
                otp.save()
                # send_sms(otp.code,otp.phone)
                return Response(
                    {"success":"the code has been successfully sent to your phone"},
                    status = status.HTTP_200_OK
                )

            else:
                otp = PhoneOtp.objects.create(phone=phone,code=random.randint(9999,99999))
                # send_sms(otp.code,otp.phone)
                return Response(
                    {"success":"the code has been successfully sent to your phone"},
                    status = status.HTTP_200_OK
                )
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)




class RegisterView(APIView):
    def post(self,request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data.get("phone")
            phoneotp = PhoneOtp.objects.get(phone=phone)
            code = request.data.get("code")
            if phoneotp.code == int(code):
                user = serializer.save()
                phoneotp.delete()
                token = AuthToken.objects.create(user=user)
                return Response({"user":user.phone},headers={"Authorization":f"Token {token[1]}"},status=status.HTTP_201_CREATED)
            else:
                return Response({"failed":"wrong code"},status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)




class LoginView(APIView):
    def post(self,request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            token = AuthToken.objects.create(user=user)
            return Response(headers={"Authorization":f"Token {token[1]}"},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        user = get_object_or_404(CustomUser,phone=request.user.phone)
        serializer = UserInfoSerializer(user)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def put(self,request):
        user = get_object_or_404(CustomUser,phone=request.user.phone)
        serializer = UserInfoSerializer(user,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
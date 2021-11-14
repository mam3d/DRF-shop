from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from ..models import CustomUser, PhoneOtp
import random
from .serializers import PhoneSerializer
from kavenegar import *



def send_sms(code,phone):
    api = KavenegarAPI('456A67346D4E4E5476636657356F6B784D6E36507653394D586B6D342F6F656B6A756D49347261384C2F303D')
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
            user_qs = CustomUser.objects.filter(phone=phone)
            if user_qs:
                return Response(
                    {"error":"user with this phone number already exist"},
                    status=status.HTTP_400_BAD_REQUEST)
                    
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




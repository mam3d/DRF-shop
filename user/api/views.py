import random
from rest_framework import (
    permissions,
    response,
    status,
    views,
    generics
    )
from knox.models import AuthToken
from ..models import (
    CustomUser,
    PhoneOtp
    )
from .serializers import (
    PhoneVerifySerializer,
    UserRegisterSerializer,
    LoginSerializer,
    UserInfoSerializer
    )
from ..helpers import send_sms


class PhoneVerifyCreate(generics.CreateAPIView):
    serializer_class = PhoneVerifySerializer

    def create(self,request,*args, **kwargs):
        super().create(request,*args, **kwargs)
        return response.Response(
            {"success":"code has been sent to your phone"},
            status=status.HTTP_201_CREATED
            )

    def perform_create(self, serializer):
        phone = serializer.validated_data.get("phone")
        code = random.randint(9999,99999)
        phone_queryset = PhoneOtp.objects.filter(phone=phone)
        if phone_queryset.exists():
            phone_verify = phone_queryset[0]
            phone_verify.code = code
            phone_verify.count += 1
            phone_verify.save()
            # send_sms(code,phone)
        else:      
            serializer.save(code=code)
            # send_sms(code,phone)

class RegisterView(generics.CreateAPIView):
    def create(self, request, *args, **kwargs):
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        token = AuthToken.objects.create(user=user)
        return response.Response(
            {
                "token":token[1]
            },
        status = status.HTTP_201_CREATED
        )
        
    def perform_create(self, serializer):
        user = serializer.save()
        return user


class LoginView(views.APIView):
    def post(self,request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = AuthToken.objects.create(user=serializer.validated_data)
        return response.Response({
            "token":token[1]
        })



class UserInfoView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserInfoSerializer
    queryset = CustomUser.objects.all()
    lookup_field = None

    def get_object(self):
        return self.request.user
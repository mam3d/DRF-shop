from django.core.cache import cache
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
    )
from .serializers import (
    PhoneVerifySerializer,
    UserRegisterSerializer,
    LoginSerializer,
    UserInfoSerializer
    )

from ..helpers import send_sms


class PhoneVerifyCreate(views.APIView):
    def post(self, request):
        serializer = PhoneVerifySerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data["phone"]
            code = phone = serializer.validated_data["code"]
            cache.set(phone, code)
            return response.Response(f"code has been sent to {phone}")
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
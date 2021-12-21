
from django.urls import path
from .views import (
    PhoneVerifyCreate,
    RegisterView,
    LoginView,
    UserInfoView
)
from knox.views import LogoutView

urlpatterns = [
    path("validate-phone/",PhoneVerifyCreate.as_view(),name="validate_phone"),
    path("register/",RegisterView.as_view(),name="register"),
    path("user/info/",UserInfoView.as_view(),name="user-info"),
    path("login/",LoginView.as_view(),name="login"),
    path("logout/", LogoutView.as_view(), name='knox_logout'),
]

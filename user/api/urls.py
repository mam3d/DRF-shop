
from django.urls import path
from .views import ValidatePhone,RegisterView, LoginView,UserInfoView
from knox.views import LogoutView

urlpatterns = [
    path("validate-phone/",ValidatePhone.as_view(),name="validate-phone"),
    path("register/",RegisterView.as_view(),name="register"),
    path("user/info/",UserInfoView.as_view(),name="user-info"),
    path("login/",LoginView.as_view(),name="login"),
    path("logout/", LogoutView.as_view(), name='knox_logout'),
]

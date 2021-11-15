
from django.urls import path
from .views import ValidatePhone,RegisterView, LoginView
from knox.views import LogoutView

urlpatterns = [
    path("validate-phone/",ValidatePhone.as_view(),name="validate-phone"),
    path("register/",RegisterView.as_view(),name="register"),
    path("login/",LoginView.as_view(),name="login"),
    path("logout/", LogoutView.as_view(), name='knox_logout'),
]

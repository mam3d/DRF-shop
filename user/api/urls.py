
from django.urls import path
from .views import ValidatePhone,RegisterView

urlpatterns = [
    path("validate-phone/",ValidatePhone.as_view(),name="validate-phone"),
    path("register/",RegisterView.as_view(),name="register"),
]

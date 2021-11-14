
from django.urls import path
from .views import ValidatePhone

urlpatterns = [
    path("validate-phone/",ValidatePhone.as_view(),name="validate-phone"),
]

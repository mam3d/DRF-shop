from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm

@admin.register(CustomUser)
class UserAdmin(UserAdmin):
    list_display = ["phone","username","date_joined","is_staff","is_admin"]
    list_filter = ["is_staff","date_joined"]
    search_field = ["phone"]
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    fieldsets = (
        (None, {
            "fields": (
                ("phone","password","is_staff","is_admin","username")
            ),
        }),
    )
    add_fieldsets = (
        (None, {
            "fields": (
                ("phone","password1","password2","is_admin","is_staff")
            ),
        }),
    )
    


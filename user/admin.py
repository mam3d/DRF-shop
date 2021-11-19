from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, PhoneOtp
from .forms import CustomUserCreationForm, CustomUserChangeForm

@admin.register(CustomUser)
class UserAdmin(UserAdmin):
    list_display = ["phone","name","date_joined","address","postal_code","is_staff",]
    list_filter = ["is_staff","date_joined"]
    search_field = ["phone"]
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    ordering = ["date_joined"]
    fieldsets = (
        (None, {
            "fields": (
                ("phone","password","is_staff","is_admin","name","address","postal_code")
            ),
        }),
    )
    add_fieldsets = (
        (None, {
            "fields": (
                ("phone","password1","password2","is_admin","is_staff","address","postal_code")
            ),
        }),
    )
    
admin.site.register(PhoneOtp)

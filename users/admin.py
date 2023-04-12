from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from users.forms import CustomUserCreationForm, CustomUserChangeForm
from users.models import CustomUser, Profile, Wishlist


class CustomUserAdmin(UserAdmin):
    # form = CustomUserCreationForm
    # add_form = CustomUserCreationForm
    # form = CustomUserChangeForm
    model = CustomUser
    list_display = ["email", "username", "is_vip", "country", "is_active", "newsLetter"]
    fieldsets = (
        *UserAdmin.fieldsets,  # original form fieldsets, expanded
        (  # new fieldset added on to the bottom
            # group heading of your choice; set to None for a blank space instead of a header
            "Extra Fields",
            {
                "fields": (
                    "is_vip",
                    "vip_date_from",
                    "city",
                    "province",
                    "country",
                    "mobile",
                    "newsLetter",
                ),
            },
        ),
    )


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Profile)
admin.site.register(Wishlist)

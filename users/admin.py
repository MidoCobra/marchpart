from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from users.forms import CustomUserCreationForm, CustomUserChangeForm
from users.models import CustomUser, Profile, Wishlist, Money_Prize

from django.utils.translation import gettext_lazy as _
import datetime

class UserEmptyEmailFilter(admin.SimpleListFilter):
    title = ('filter email')
    parameter_name = 'email'
    def lookups(self, request, model_admin):
       return (
           ('NoEmail', _('No Email Added')),
           ('EmailExists', _('Email Added')),
            )
    def queryset(self, request, queryset):
        if self.value() == 'NoEmail':
            return queryset.filter(email='')
        if self.value() == 'EmailExists':
            return queryset.filter(email__isnull=False)

class CustomUserAdmin(UserAdmin):
    # form = CustomUserCreationForm
    # add_form = CustomUserCreationForm
    # form = CustomUserChangeForm
    model = CustomUser
    list_display = ["email", "username", "is_vip", "country", "is_active", "newsLetter"]
    list_filter = [UserEmptyEmailFilter, 'is_staff']
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

class DateFilter_Offers(admin.SimpleListFilter):
    
    title = ('filter by valid dates')
    parameter_name = 'validty'
    def lookups(self, request, model_admin):
       return (
           ('valid', _('Valid Offers')),
           ('Not_valid', _('Expired Offers')),
            )
    def queryset(self, request, queryset):
        date = datetime.date.today()
        if self.value() == 'valid':
            return queryset.filter(valid_to__gte=date)
        if self.value() == 'Not_valid':
            return queryset.filter(valid_to__lt=date)

class MoneyPrizeAdmin(admin.ModelAdmin):
    model = Money_Prize
    autocomplete_fields = ["user"]
    list_display = ['user', 'amount' ,'valid_from' ,'valid_to']  
    list_filter = [DateFilter_Offers,]
    search_fields = ['user']

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Profile)
admin.site.register(Wishlist)
admin.site.register(Money_Prize, MoneyPrizeAdmin)




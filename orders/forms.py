from django import forms
from .models import Order, ShippingCosts


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'first_name', 
            'last_name', 
            'email', 
            'address', 
            'postal_code', 
            'city',
            'phone1', 
            'phone2', 
            'country', 
            'promo_code'
            ]

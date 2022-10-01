from django.forms import ModelForm
from .models import ReviewProduct, Model, Product, ContactUs, Merchant_Request
from django import forms


class ReviewProductForm(ModelForm):
    class Meta:
        model = ReviewProduct
        fields = ["comment", "rate"]
        widgets = {
            "comment": forms.Textarea(
                attrs={
                    "cols": 60,
                    "rows": 3,
                    "id": "post-text",
                    "required": True,
                    "placeholder": "Review Product...",
                }
            ),
        }


class ContactUsForm(ModelForm):
    class Meta:
        model = ContactUs
        fields = '__all__'

class Merchant_Request_Form(ModelForm):
    class Meta:
        model = Merchant_Request
        fields = '__all__'
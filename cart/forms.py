from django import forms


PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 26)]


class CartAddProductForm(forms.Form):

    quantity = forms.IntegerField(widget=forms.TextInput(attrs={
        'id':'quantity',
        # 'min_value':1,
        })
        )
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput(attrs={
        'id':'update',
        # 'min_value':1,
        })
        )

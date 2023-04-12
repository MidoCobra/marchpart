from django import forms


PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 26)]


class CartAddProductForm(forms.Form):
    # quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int)
    # update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)

    quantity = forms.IntegerField(widget=forms.TextInput(attrs={
        'id':'quantity',
        # 'min_value':1,
        })
        )
    # quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int,widget=forms.Select(attrs={'id':'quantity'}))
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput(attrs={
        'id':'update',
        # 'min_value':1,
        })
        )

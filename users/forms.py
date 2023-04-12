from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import CustomUser

from django.forms import ModelForm, Textarea, TextInput
# from django.views.generic import FormView, RedirectView

# class LoginForm(AuthenticationForm):
#     username= forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
#     password= forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))


class CustomUserCreationForm(UserCreationForm):
    agreement = forms.BooleanField(required=True)
    email = forms.EmailField(
        max_length=254, help_text='Required. Inform a valid email address.')

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = (
            'username', 'email', 'first_name', 'last_name', 'country', 'photo', 'password1', 'password2',
            'agreement', 'is_vip', 'province',  'city', 'mobile', 'newsLetter'
        )
        widgets = {

            'email': TextInput(attrs={'required': 'true'}),
            # 'first_name' :TextInput(attrs={'class':'form-control'}),
            # 'last_name' :TextInput(attrs={'class':'form-control'}),
            # 'country' :TextInput(attrs={'class':'form-control'}),
        }

    # for unique email and username accounts:

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and CustomUser.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError(
                u'Email addresse already exists!, Try another one.')
        return email


class CustomUserChangeForm(UserChangeForm):
    # email =  forms.CharField(disabled=True)
    # date_joined = forms.DateField(disabled=True)
    class Meta:
        model = CustomUser
        fields = UserChangeForm.Meta.fields


class UpdateAccountForm(forms.ModelForm):

    # create meta class
    class Meta:
        # specify model to be used
        model = CustomUser

        # specify fields to be used
        fields = [
            "city",
            "province",
            "country",
            "mobile",
            "newsLetter",
        ]


class LoginForm(AuthenticationForm):
    pass


class LoginArabicForm(forms.Form):
    username = forms.CharField(label='بريدك الإليكترونى', max_length=100)
    password = forms.CharField(label='كلمة السر', max_length=100)



class UserDeactivateForm(forms.Form):
    """
    Simple form that provides a checkbox that signals deactivation.
    """
    deactivate = forms.BooleanField(required=True)


class UserDeleteForm(forms.Form):
    """
    Simple form that provides a checkbox that signals deletion.
    """
    delete = forms.BooleanField(required=True)
from .models import PhotosUploader
from django import forms

class PhotoForm(forms.ModelForm):
    class Meta:
        model = PhotosUploader
        fields = ('file', )
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views import View

from .forms import PhotoForm
from .models import PhotosUploader

class BasicUploadView(View):
    def get(self, request):
        if request.user.is_authenticated and (
            request.user.email == "mgbnmichael@yahoo.com" or request.user.email == "Bishoynady@outlook.com" or request.user.email == "sales@desertcameldev.com"
            ):
            photos_list = PhotosUploader.objects.all().order_by('-uploaded_at')[:100]
            return render(self.request, 'photosUploader.html', {'photos': photos_list})
        else:
            return JsonResponse({'Not For You': 'Don\'t PLay'})

    def post(self, request):
        form = PhotoForm(self.request.POST, self.request.FILES)
        if form.is_valid() and (request.user.is_authenticated and (request.user.email == "mgbnmichael@yahoo.com" or request.user.email == "Bishoynady@outlook.com" or request.user.email == "sales@desertcameldev.com")):
            photo = form.save()
            data = {'is_valid': True, 'name': photo.file.name, 'url': photo.file.url}
        else:
            data = {'is_valid': False}
    
            # return HttpResponse('Sorry! You are not allowed to add photos')


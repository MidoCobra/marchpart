from django.conf.urls import url
from django.urls import re_path, path
from . import views

app_name = 'photos'

urlpatterns = [
    re_path(r'^basic-upload/$', views.BasicUploadView.as_view(), name='basic_upload'),
]
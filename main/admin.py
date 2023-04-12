from django.contrib import admin
from .models import HomePage_main_banners, PhotosUploader, HomePage_main_banners_WEBSITE


# # called after page validation, to switch page (we catch the ValidationError send from save_model
# # if this image was already uploaded
# def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
#     try:
#         return super(MediaAdmin, self).changeform_view(request, object_id, form_url, extra_context)
#     except ValidationError as e:
#         self.message_user(request, e, level=messages.ERROR)
#         if object_id:
#             # if we are editing an existing media
#             return redirect(to=reverse('admin:web_app_media_change', args=(object_id, )))
#         else:
#             # if we try to add a new media
#             return redirect(to=reverse('admin:web_app_media_add'))

# # check if the media was uploaded before, and raise a ValidationError if it's the case
# def save_model(self, request, obj, form, change):
#     if not obj.hash:
#         obj.hash = imagehash.average_hash(Image.open(obj.media)).__str__()

#     duplicate = False
#     for media in Media.objects.all():
#         if media.media != obj.media and media.hash == obj.hash:
#             duplicate = True

#     if not duplicate:
#         super(MediaAdmin, self).save_model(request, obj, form, change)
#     else:
#         raise ValidationError("This media was already uploaded.")



admin.site.register(HomePage_main_banners)
admin.site.register(HomePage_main_banners_WEBSITE)

# admin.site.register(PhotosUploader)

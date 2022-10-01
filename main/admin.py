from django.contrib import admin
from .models import HomePage_main_banners, PhotosUploader, HomePage_main_banners_WEBSITE, Offer_category, Offer_product, NewsLetter_Photo
from django.utils.translation import gettext_lazy as _
import datetime

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


class OfferProductAdmin(admin.ModelAdmin):
    autocomplete_fields = ["product"]
    list_display = ['product' ,'valid_from' ,'valid_to']  
    list_filter = ['offer_category__name' ,DateFilter_Offers]
    search_fields = ['product__name']  



admin.site.register(HomePage_main_banners)
admin.site.register(HomePage_main_banners_WEBSITE)
admin.site.register(Offer_category)
admin.site.register(Offer_product, OfferProductAdmin)
admin.site.register(NewsLetter_Photo)

# admin.site.register(PhotosUploader)

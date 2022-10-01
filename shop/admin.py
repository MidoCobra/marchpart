from django.contrib import admin
from .models import *
from .custom_filter import DuplicatSlugFilter
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin
from import_export.admin import ImportExportActionModelAdmin
from import_export.widgets import JSONWidget, ManyToManyWidget, ForeignKeyWidget
from django.utils.translation import gettext_lazy as _


class SaleFilter(admin.SimpleListFilter):
    title = ('filter 0 sale prices')
    parameter_name = 'sale_price'
    def lookups(self, request, model_admin):
       return (
           ('Zero', _('sale price Zero')),
           ('Not_Zero', _('sale price is not zero')),
            )
    def queryset(self, request, queryset):
        if self.value() == 'Zero':
            return queryset.filter(sale_price=0)
        if self.value() == 'Not_Zero':
            return queryset.exclude(sale_price=0)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}


class BrandAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}


class ModelAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ["name"]
    list_display = ["name", "slug"]
    list_filter = (DuplicatSlugFilter,)




# class ProductOperationsWidget(ManyToManyWidget):

#     def render(self, value, obj=None):
#         return json.dumps(
#             list(value.values('identifier', 'operator', 'value')),
#         )

class ProductResource(resources.ModelResource): 
    model = fields.Field(
        attribute='model',
        widget=ManyToManyWidget(model=Model, separator=',', field='name'),
    )   
    manfacture_date = fields.Field(
        attribute='manfacture_date',
        widget=ManyToManyWidget(model=ManfactureDate, separator=',', field='manfacture_year'),
    )   
    engine_capacity = fields.Field(
        attribute='engine_capacity',
        widget=ForeignKeyWidget(model=EngineCapacity, field='eng_capacity'),
    )   
    category = fields.Field(
        attribute='category',
        widget=ForeignKeyWidget(model=Category, field='name'),
    )   
    class Meta:
        model = Product
        # fields = ('engine_capacity__eng_capacity','name_arabic', 'name', 'model__name')
        exclude = ('created_at','updated_at' )

    # def __init__(self):
    #     super(ProductResource, self).__init__()
    #     # Introduce a class variable to pass dry_run into methods that do not get it
    #     self.in_dry_run = False

    # def before_import(self, dataset, using_transactions, dry_run, **kwargs):
    #     # Set helper class method to dry_run value
    #     self.in_dry_run = dry_run

    # def before_import_row(self, row, row_number=None, **kwargs):
    #     if not self.in_dry_run:
    #         # Get URL and split image name from import file
    #         image_url = row['portrait']
    #         image_name = image_url.split('/')[-1]

    #         # Generate temporary file and download image from provided URL
    #         tmp_file = NamedTemporaryFile(delete=True, dir=f'{settings.MEDIA_ROOT}')
    #         tmp_file.write(urllib.request.urlopen(image_url).read())
    #         tmp_file.flush()

    #         # Add file object to row
    #         row['portrait'] = File(tmp_file, image_name)
class MyModelInline(admin.TabularInline):
     model = Category
     classes = ['collapse']

class ProductAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    fieldsets = (
         
                ('Product', { 
                'fields': ( ('model', 'engine_capacity', 'manfacture_date','category'), ('name', 'name_arabic','slug'), 
                ( 'product_commercial_name', 'product_commercial_name_arabic'),
                'part_number', 'part_brand',
             
                'made_in', 'made_in_arabic', 'description', 'description_arabic', 'features', 'features_arabic',( 'price', 'sale_price'),
                ('max_per_order', 'min_per_order'), ('available','seller_recommendation', 'hidden', 'free_shipping'), 'stock', 'image', 'image2',
                'image3', 'image4', 'image5', 'youtube_link', 'search_tags', 'meta_description',
                )
                }),
                ('Tires', { 
                'description' : 'Add Tires Specs',
                # 'classes' : ('collapse',),
                'fields': ('tires','tire_rim_size', 'tire_height_num', 'tire_width_num')
               
                }),
                ('Liquids', { 
                'description' : 'Add Liquids Specs',
                # 'classes' : ('collapse',),
                'fields': ('liquids','liquid_type')
               
                }),
    )
    list_display = ["name", "price", "sale_price", "available", 'image_tag']
    list_filter = ["available", "created_at", "updated_at", "category", "model", SaleFilter,'liquids', 'tires', 'model__brand']
    list_editable = ["price", "sale_price", "available"]
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = [
        "id",
    ]
    search_fields = ["model__name", "name", 'slug']
    autocomplete_fields = ["model"]
    resource_class = ProductResource
    

class ContactUsAdmin(admin.ModelAdmin):
    list_display = ['name','email', 'answered', 'closed']
    list_filter = ['answered', 'closed']
    search_fields = ['name','email']

def send_newsletter(modeladmin, request, queryset):
    for newsletter in queryset:
        newsletter.send(request)


send_newsletter.short_description = "Send selected Newsletters to all subscribers"


class NewsletterAdmin(admin.ModelAdmin):
    actions = [send_newsletter]


class HomePage_addsAdmin(admin.ModelAdmin):
    autocomplete_fields = ["product"]


class HomePage_bannersAdmin(admin.ModelAdmin):
    autocomplete_fields = ["product"]




admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(ManfactureDate)
admin.site.register(Model, ModelAdmin)
admin.site.register(EngineCapacity)
admin.site.register(HomePage_adds, HomePage_addsAdmin)
admin.site.register(HomePage_banners, HomePage_bannersAdmin)
admin.site.register(ReviewProduct)
admin.site.register(Blog_tags)
admin.site.register(Blog)
admin.site.register(Part_Brand)

admin.site.register(Rim_size)
admin.site.register(Tire_height)
admin.site.register(Tire_width)

admin.site.register(Liquid_type)
admin.site.register(ContactUs, ContactUsAdmin)
admin.site.register(Terms_and_privacy)
admin.site.register(Contact_information)
admin.site.register(Newsletter, NewsletterAdmin)
admin.site.register(Merchant_Request)

# admin.site.register(Shipping)

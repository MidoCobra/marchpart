# from django.contrib import admin
# from .models import *

# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ['name', 'slug']
#     prepopulated_fields = {'slug': ('name',)}

# class BrandAdmin(admin.ModelAdmin):
#     list_display = ['name', 'slug']
#     prepopulated_fields = {'slug': ('name',)}

# class ModelAdmin(admin.ModelAdmin):
#     prepopulated_fields = {'slug': ('name',)}


# class ProductAdmin(admin.ModelAdmin):
#     list_display = ['name', 'model', 'price', 'stock', 'available', 'created_at']
#     list_filter = ['available', 'created_at', 'updated_at', 'category', 'model']
#     list_editable = ['price', 'stock', 'available']
#     prepopulated_fields = {'slug': ('name',)}


# admin.site.register(Product, ProductAdmin)
# admin.site.register(Category, CategoryAdmin)
# admin.site.register(Brand, BrandAdmin)
# admin.site.register(ManfactureDate)
# admin.site.register(Model, ModelAdmin)
# admin.site.register(EngineCapacity)
# admin.site.register(ReviewProduct)

# # admin.site.register(Shipping)

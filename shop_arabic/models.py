# from django.db import models
# from django.urls import reverse
# import datetime
# from django.core.validators import MaxValueValidator, MinValueValidator
# # for star ratings:
# from django.contrib.contenttypes.fields import GenericRelation
# from star_ratings.models import Rating, AbstractBaseRating, UserRating


# def current_year():
#     return (datetime.date.today().year) + 1


# def max_value_current_year(value):
#     return MaxValueValidator(current_year())(value)


# class Brand(models.Model):
#     name = models.CharField(max_length=150, unique=True, db_index=True)
#     slug = models.SlugField(max_length=100, db_index=True, null=True)
#     image = models.ImageField('photo 160x110', upload_to='media/')

#     def __str__(self):
#         return self.name

#     def get_absolute_url(self):
#         return reverse('shop:models', args=[self.slug])


# class Model(models.Model):
#     brand = models.ForeignKey(
#         Brand, on_delete=models.CASCADE, related_name="models")
#     name = models.CharField(max_length=150, db_index=True, unique=True)
#     slug = models.SlugField(max_length=100, db_index=True, null=True)
#     image = models.ImageField('photo 640x400', upload_to='media/')

#     def __str__(self):
#         return '{} - {}'.format(self.name, self.brand.name)

#     def get_absolute_url(self):
#         return reverse('shop:model_categories', args=[self.slug])


# class EngineCapacity(models.Model):
#     eng_capacity = models.IntegerField(('سعة الموتور'), validators=[
#                                        MinValueValidator(100), MaxValueValidator(8000)], null=True, unique=True)

#     def __str__(self):
#         return str(self.eng_capacity)


# class ManfactureDate(models.Model):
#     manfacture_year = models.IntegerField(('year'), validators=[MinValueValidator(
#         1980), max_value_current_year], null=True, unique=True)

#     def __str__(self):
#         return str(self.manfacture_year)


# class Category(models.Model):
#     # model = models.ForeignKey(Model, on_delete=models.CASCADE, related_name="categories")
#     name = models.CharField(max_length=150, db_index=True)
#     slug = models.SlugField(max_length=150, unique=True, db_index=True)
#     image = models.ImageField('photo 180x180', upload_to='media/')
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         ordering = ('name', )
#         verbose_name = 'Part Type'
#         verbose_name_plural = 'Part Types'

#     def __str__(self):
#         return self.name

#     def get_absolute_url(self):
#         return reverse('shop:all_product_list_by_category', args=[self.slug])

#     def get_absolute_url_for_model(self):
#         return reverse('shop:product_list_by_category', args=[self.products.model.slug])


# class Product(models.Model):
#     # brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name="partTypesBrand", null=True, blank=True)
#     model = models.ForeignKey(Model, on_delete=models.PROTECT,
#                               related_name="partTypesModel", null=True, blank=True)
#     engine_capacity = models.ForeignKey(
#         EngineCapacity, on_delete=models.PROTECT, related_name="partTypesEngCap", null=True, blank=True)
#     manfacture_date = models.ManyToManyField(ManfactureDate, blank=True)
#     category = models.ForeignKey(
#         Category, related_name='products', on_delete=models.CASCADE)
#     name = models.CharField(max_length=100, db_index=True)
#     slug = models.SlugField(max_length=100, db_index=True)
#     description = models.TextField(blank=True)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     sale_price = models.DecimalField(
#         max_digits=10, decimal_places=2, null=True, blank=True, help_text="just leave this field blank if no sale available"
#     )
#     available = models.BooleanField(default=True)
#     max_per_order = models.PositiveIntegerField(default=1)
#     min_per_order = models.PositiveIntegerField(default=1)
#     stock = models.PositiveIntegerField(null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     image = models.ImageField('photo 270x270', upload_to='media/', blank=False)
#     image2 = models.ImageField(
#         'photo 270x270', upload_to='media/', null=True, blank=True)
#     image3 = models.ImageField(
#         'photo 800x800', upload_to='media/', null=True, blank=True)
#     image4 = models.ImageField(
#         'photo 800x800', upload_to='media/', null=True, blank=True)
#     image5 = models.ImageField(
#         'photo 800x800', upload_to='media/', null=True, blank=True)
#     youtube_link = models.URLField(null=True)

#     rate_product = GenericRelation(Rating, related_query_name='product_rate')

#     class Meta:
#         ordering = ('name', )
#         index_together = (('id', 'slug'),)

#     def __str__(self):
#         return self.name

#     def get_absolute_url(self):
#         return reverse('shop:product_detail', args=[self.id, self.slug])


# class ReviewProduct(models.Model):
#     product = models.CharField(max_length=100)
#     pub_date = models.DateTimeField('date published', auto_now=True)
#     user_name = models.CharField(max_length=100)
#     comment = models.TextField(max_length=250)
#     Reply = models.TextField(max_length=300, null=True, blank=True)
#     # avatar = models.URLField(null=True, blank=True)
#     # ip = models.GenericIPAddressField(blank=True, null=True)
#     rate = models.ForeignKey(UserRating, on_delete=models.CASCADE, null=True)

#     def __str__(self):
#         return self.user_name

# # class HomePageAds(models.Model):
# #     product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
# #     slide_title = models.CharField(max_length=154, null=True, blank=True)
# #     slide_short_Descrip_1 = models.TextField(max_length=154, null=True, blank=True)
# #     slide_short_Descrip_2 = models.TextField(max_length=154, null=True, blank=True)
# #     slide_short_Descrip_3 = models.TextField(max_length=154, null=True, blank=True)
# #     slide_image = models.ImageField(upload_to='media/',null=True, blank=True)
# #     price_of_item = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
# #     discount_percent = models.CharField (max_length=154,null=True,blank=True)

# #     def __str__(self):
# #         return self.slide_title

# # class AddInfo(models.Model):
# #     name = models.CharField(max_length=154, default='info')
# #     support_email_1 = models.EmailField(null=True,blank=True)
# #     support_email_2 = models.EmailField(null=True,blank=True)
# #     support_Phone_1 = models.CharField (max_length=154,null=True,blank=True)
# #     support_Phone_2 = models.CharField (max_length=154,null=True,blank=True)

# #     def __str__(self):
# #         return self.name

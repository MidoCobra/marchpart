from django.db import models
from shop.models import Product
from django.urls import reverse

class HomePage_main_banners(models.Model):
    link_english = models.URLField()
    link_arabic = models.URLField()
    banner_title = models.CharField(max_length=154)
    search_key = models.CharField(max_length=154, null=True)
    banner_image = models.ImageField("Photo 1920x720", upload_to="media/")

    def __str__(self):
        return self.banner_title
    class Meta:
        verbose_name = "Home Page Main Banner (Mobile Apps)"
        verbose_name_plural = "Home Page Main Banners (Mobile Apps)"

class HomePage_main_banners_WEBSITE(models.Model):
    link_english = models.URLField()
    link_arabic = models.URLField()
    banner_title = models.CharField(max_length=154)
    banner_image = models.ImageField("Photo 1920x720", upload_to="media/")

    def __str__(self):
        return self.banner_title


class PhotosUploader(models.Model):
    title = models.CharField(max_length=255, blank=True)
    file = models.ImageField(upload_to='media/')
    uploaded_at = models.DateTimeField(auto_now_add=True)    


class Offer_category(models.Model):
    name = models.CharField(max_length=255)
    name_arabic = models.CharField(max_length=255)

    def get_absolute_url(self):
        return reverse("shop:offer_products", args=[self.id])

    def get_absolute_url_arabic(self):
        return reverse(
            "shop_arabic:offer_products_arabic", args=[self.id]
        )
    def  __str__(self):
        return self.name

class Offer_product(models.Model):
    offer_category = models.ForeignKey(Offer_category, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    valid_from = models.DateField()
    valid_to = models.DateField()

    def  __str__(self):
        return self.product.name_arabic


class NewsLetter_Photo(models.Model):
    title = models.CharField(max_length=255)
    file = models.ImageField(upload_to='media/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
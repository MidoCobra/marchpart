from django.db import models


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
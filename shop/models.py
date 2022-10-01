from django.db import models
from django.urls import reverse
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator

# for star ratings:
from django.contrib.contenttypes.fields import GenericRelation
from star_ratings.models import Rating, AbstractBaseRating, UserRating
from django.conf import settings
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.contrib.auth import get_user_model
from django.utils.safestring import mark_safe

from .validators import validate_file_extension

def current_year():
    return (datetime.date.today().year) + 1


def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)


class Brand(models.Model):
    name = models.CharField(max_length=150, unique=True, db_index=True)
    slug = models.SlugField(max_length=100, db_index=True, null=True, unique=True)
    name_arabic = models.CharField(max_length=150, null=True, db_index=True)
    image = models.ImageField("photo 160x110", upload_to="media/")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("shop:models", args=[self.slug])

    def get_absolute_url_arabic(self):
        return reverse("shop_arabic:models_arabic", args=[self.slug])


class Model(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="models")
    name = models.CharField(max_length=150, db_index=True, unique=True)
    slug = models.SlugField(max_length=100, db_index=True, null=True, unique=True)
    name_arabic = models.CharField(max_length=150, null=True, unique=True)
    image = models.ImageField("photo 640x400", upload_to="media/")

    def __str__(self):
        return "{} - {}".format(self.name, self.brand.name)

    def get_absolute_url(self):
        return reverse("shop:model_categories", args=[self.slug])

    def get_absolute_url_arabic(self):
        return reverse("shop_arabic:model_categories_arabic", args=[self.slug])


class EngineCapacity(models.Model):
    eng_capacity = models.IntegerField(
        ("سعة الموتور"),
        validators=[MinValueValidator(100), MaxValueValidator(8000)],
        null=True,
        unique=True,
    )

    def __str__(self):
        return str(self.eng_capacity)


class ManfactureDate(models.Model):
    manfacture_year = models.IntegerField(
        ("year"),
        validators=[MinValueValidator(1890), max_value_current_year],
        null=True,
        unique=True,
    )

    def __str__(self):
        return str(self.manfacture_year)


class Category(models.Model):
    # model = models.ForeignKey(Model, on_delete=models.CASCADE, related_name="categories")
    name = models.CharField(max_length=150, db_index=True, unique=True)
    name_arabic = models.CharField(max_length=150, null=True, unique=True)
    slug = models.SlugField(max_length=150, unique=True, db_index=True)
    image = models.ImageField("photo 180x180", upload_to="media/")
    # image2 = models.ImageField('photo 180x180', upload_to='media/', null=True)
    category_banner = models.ImageField("photo 870x220", upload_to="media/", null=True)
    category_leftSide_image = models.ImageField(
        "photo 270x420", upload_to="media/", null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("name",)
        verbose_name = "Part Type"
        verbose_name_plural = "Part Types"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("shop:all_product_list_by_category", args=[self.slug])

    def get_absolute_url_arabic(self):
        return reverse(
            "shop_arabic:all_product_list_by_category_arabic", args=[self.slug]
        )

    def get_absolute_url_for_model(self):
        return reverse("shop:product_list_by_category", args=[self.products.model.slug])

class Part_Brand(models.Model):
    name = models.CharField(max_length=400)
    name_arabic = models.CharField(max_length=400)
    liquid = models.BooleanField("Is Liquid", default=False)
    image = models.ImageField("photo 270x270",help_text="add photo if the brand is of liquids and oils only", upload_to="media/",null=True, blank=True)

    def get_absolute_url_arabic(self):
        return reverse("shop_arabic:liquids_types_arabic", args=[self.id,])

    def get_absolute_url(self):
        return reverse("shop:liquids_types", args=[self.id,])

    def get_absolute_url_all_brands_arabic(self):
        return reverse("shop_arabic:part-brand_arabic", args=[self.id,])

    def __str__(self):
        return self.name

class Liquid_type(models.Model):
    # brand = models.ForeignKey(Part_Brand, on_delete=models.CASCADE, related_name="part_Brand_Liquid_Type")
    name = models.CharField(max_length=400)
    name_arabic = models.CharField(max_length=400)
    image = models.ImageField("photo 270x270", upload_to="media/",null=True, blank=True)

    def get_absolute_url_arabic(self):
        return reverse("shop_arabic:liquids_products_arabic", args=[self.id])

    def get_absolute_url(self):
        return reverse("shop:liquids_products", args=[self.id])

    def __str__(self):
        return self.name    


class Rim_size(models.Model):
    rim_size = models.CharField(max_length=5, unique=True)
    def __str__(self):
        return self.rim_size  

class Tire_height(models.Model):
    tire_height = models.CharField(max_length=5, unique=True)
    def __str__(self):
        return self.tire_height  

class Tire_width(models.Model):
    tire_width = models.CharField(max_length=5, unique=True)
    def __str__(self):
        return self.tire_width  

class Product(models.Model):
    # brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name="partTypesBrand", null=True, blank=True)
    model = models.ManyToManyField(
        Model,
        # on_delete=models.PROTECT,
        related_name="partTypesModel",
        # null=True,
        blank=True,
    )
    engine_capacity = models.ForeignKey(
        EngineCapacity,
        on_delete=models.PROTECT,
        related_name="partTypesEngCap",
        null=True,
        blank=True,
    )
    manfacture_date = models.ManyToManyField(ManfactureDate,related_name="manfYears", blank=True)
    category = models.ForeignKey(
        Category, related_name="products", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=200, db_index=True, unique=True)
    slug = models.SlugField(
        max_length=100,
        db_index=True,
        unique=True,
        help_text="This field will be filled automatically",
    )
    name_arabic = models.CharField(max_length=200, null=True, unique=True)
    part_brand = models.ForeignKey(Part_Brand, related_name="partbrand",on_delete=models.CASCADE, null=True)
    product_commercial_name = models.CharField(max_length=200, null=True)
    product_commercial_name_arabic = models.CharField(max_length=200, null=True)
    made_in = models.CharField(max_length=100, null=True)
    made_in_arabic = models.CharField(max_length=100, null=True)
    description = models.TextField(null=True, blank=True)
    description_arabic = models.TextField(null=True, blank=True)
    features = models.TextField(null=True, blank=True)
    features_arabic = models.TextField(null=True, blank=True)
    
    tires = models.BooleanField(default=False)
    rim_size = models.CharField(max_length=5, null=True, blank=True)
    tire_height = models.CharField(max_length=5, null=True, blank=True)
    tire_width = models.CharField(max_length=5, null=True, blank=True)


    tire_rim_size = models.ForeignKey(Rim_size,on_delete=models.CASCADE, null=True, blank=True)
    tire_height_num = models.ForeignKey(Tire_height,on_delete=models.CASCADE, null=True, blank=True)
    tire_width_num = models.ForeignKey(Tire_width,on_delete=models.CASCADE, null=True, blank=True)

    liquids = models.BooleanField("Is Liquid",default=False)
    liquid_type = models.ForeignKey(Liquid_type , on_delete=models.CASCADE, related_name="liquids_Types", null=True, blank=True)
    
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="just leave this field blank if no sale available",
    )
    available = models.BooleanField(default=True)
    max_per_order = models.PositiveIntegerField(default=1)
    min_per_order = models.PositiveIntegerField(default=1)
    stock = models.PositiveIntegerField(null=True, blank=True)

    seller_recommendation = models.BooleanField(default=False)
    hidden = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    image = models.ImageField("photo 270x270", upload_to="media/", blank=False)
    image2 = models.ImageField(
        "photo 270x270", upload_to="media/", null=True, blank=False
    )
    image3 = models.ImageField(
        "photo 800x800", upload_to="media/", null=True, blank=False
    )
    image4 = models.ImageField(
        "photo 800x800", upload_to="media/", null=True, blank=False
    )
    image5 = models.ImageField(
        "photo 800x800", upload_to="media/", null=True, blank=False
    )
    youtube_link = models.URLField(null=True, blank=True)

    rate_product = GenericRelation(Rating, related_query_name="product_rate")

    search_tags = models.TextField(max_length=250, null=True, blank=True)

    part_number = models.CharField(max_length=500, null=True)

    free_shipping = models.BooleanField(default=False)

    meta_description = models.CharField(max_length=200, null=True, blank=True)
    
    class Meta:
        ordering = ("name",)
        index_together = (("id", "slug"),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("shop:product_detail", args=[self.id, self.slug])

    def get_absolute_url_arabic(self):
        return reverse("shop_arabic:product_detail_arabic", args=[self.id, self.slug])
        
    def clean(self):
        if self.sale_price == 0:
            self.sale_price = None
            return self.sale_price
    
    def  image_tag(self):
        return mark_safe('<img src="/../../media/%s" width="50" />' % (self.image))

    image_tag.allow_tags = True 

# class Liquids(models.Model):
#     brand = models.ForeignKey(Part_Brand, on_delete=models.CASCADE, related_name="part_Brand_Liquids")
#     liquid_type = models.ForeignKey(Liquid_type , on_delete=models.CASCADE, related_name="liquid_Type")
#     product = models.ForeignKey(Product , on_delete=models.CASCADE, related_name="Liquid_Product")



class ReviewProduct(models.Model):
    product = models.CharField(max_length=100)
    pub_date = models.DateTimeField("date published", auto_now=True)
    user_name = models.CharField(max_length=100)
    comment = models.TextField(max_length=250)
    Reply = models.TextField(max_length=300, null=True, blank=True)
    # avatar = models.URLField(null=True, blank=True)
    # ip = models.GenericIPAddressField(blank=True, null=True)
    rate = models.ForeignKey(UserRating, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.user_name


class HomePage_adds(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, null=True, blank=True
    )
    slide_title = models.CharField(max_length=154)
    slide_image = models.ImageField("Photo 1920x720", upload_to="media/")

    def __str__(self):
        return self.slide_title


class HomePage_banners(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, null=True, blank=True
    )
    banner_title = models.CharField(max_length=154)
    banner_image = models.ImageField("Photo 640x400", upload_to="media/")

    def __str__(self):
        return self.banner_title


class Blog_tags(models.Model):
    tag = models.CharField(max_length=200, db_index=True)
    tag_arabic = models.CharField(max_length=200, null=True)
    slug = models.SlugField(max_length=100, db_index=True, null=True, unique=True)

    def get_absolute_url(self):
        return reverse("shop:blogs_by_tag", args=[str(self.slug)])

    def get_absolute_url_arabic(self):
        return reverse("shop_arabic:blogs_by_tag_arabic", args=[str(self.slug)])

    def __str__(self):
        return self.tag


class Blog(models.Model):
    tag = models.ManyToManyField(Blog_tags)
    author = models.CharField(max_length=154)
    author_arabic = models.CharField(max_length=154, null=True)
    title = models.TextField(
        max_length=300,
        db_index=True,
    )
    title_arabic = models.TextField(max_length=300, null=True)
    slug = models.SlugField(
        "commercial title",
        max_length=100,
        db_index=True,
        help_text="This field only contains letters numbers and hyphens , No spaces",
        null=True,
        unique=True,
    )
    paragraph_1_heading = models.CharField(max_length=200, null=True, blank=True)
    paragraph_1 = models.TextField(max_length=5000)
    paragraph_2_heading = models.CharField(max_length=200, null=True, blank=True)
    paragraph_2 = models.TextField(max_length=5000, null=True, blank=True)
    paragraph_3_heading = models.CharField(max_length=200, null=True, blank=True)
    paragraph_3 = models.TextField(max_length=5000, null=True, blank=True)
    paragraph_4_heading = models.CharField(max_length=200, null=True, blank=True)
    paragraph_4 = models.TextField(max_length=5000, null=True, blank=True)
    paragraph_5_heading = models.CharField(max_length=200, null=True, blank=True)
    paragraph_5 = models.TextField(max_length=5000, null=True, blank=True)
    paragraph_6_heading = models.CharField(max_length=200, null=True, blank=True)
    paragraph_6 = models.TextField(max_length=5000, null=True, blank=True)
    paragraph_7_heading = models.CharField(max_length=200, null=True, blank=True)
    paragraph_7 = models.TextField(max_length=5000, null=True, blank=True)

    paragraph_1_heading_arabic = models.CharField(max_length=200, null=True, blank=True)
    paragraph_1_arabic = models.TextField(max_length=5000, null=True)
    paragraph_2_heading_arabic = models.CharField(max_length=200, null=True, blank=True)
    paragraph_2_arabic = models.TextField(max_length=5000, null=True, blank=True)
    paragraph_3_heading_arabic = models.CharField(max_length=200, null=True, blank=True)
    paragraph_3_arabic = models.TextField(max_length=5000, null=True, blank=True)
    paragraph_4_heading_arabic = models.CharField(max_length=200, null=True, blank=True)
    paragraph_4_arabic = models.TextField(max_length=5000, null=True, blank=True)
    paragraph_5_heading_arabic = models.CharField(max_length=200, null=True, blank=True)
    paragraph_5_arabic = models.TextField(max_length=5000, null=True, blank=True)
    paragraph_6_heading_arabic = models.CharField(max_length=200, null=True, blank=True)
    paragraph_6_arabic = models.TextField(max_length=5000, null=True, blank=True)
    paragraph_7_heading_arabic = models.CharField(max_length=200, null=True, blank=True)
    paragraph_7_arabic = models.TextField(max_length=5000, null=True, blank=True)

    youtube_link = models.URLField(null=True, blank=True)
    image = models.ImageField("Photo 900x600", upload_to="media/")
    image2 = models.ImageField("Photo 270x420", upload_to="media/")

    created_at = models.DateTimeField("Created Time", auto_now_add=True)

    def get_absolute_url(self):
        return reverse("shop:blog-details", args=[str(self.slug)])

    def get_absolute_url_arabic(self):
        return reverse("shop_arabic:blog-details_arabic", args=[str(self.slug)])

    def __str__(self):
        return "%s , %s" % (self.author, self.title)


class Newsletter(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    subject = models.CharField(max_length=150)
    contents = models.FileField(upload_to="media/uploaded_newsletters/")

    def __str__(self):
        return self.subject + " " + self.created_at.strftime("%B %d, %Y")

    def send(self, request):
        user = get_user_model()
        contents = self.contents.read().decode("utf-8")
        subscribers = user.objects.filter(newsLetter=True)
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        for sub in subscribers:
            message = Mail(
                from_email=settings.FROM_EMAIL,
                to_emails=sub.email,
                subject=self.subject,
                html_content=contents
                # + (
                #     '<br><a href="{}/delete/?email={}&conf_num={}">Unsubscribe</a>.').format(
                #         request.build_absolute_uri('/delete/'),
                #         sub.email,
                #         sub.conf_num)
            )
            sg.send(message)


class Terms_and_privacy(models.Model):
    terms_headline = models.CharField(max_length=220)
    terms_parachraph = models.TextField(max_length=40000)
    terms_release_date = models.DateField()
    privacy_headline = models.CharField(max_length=220)
    privacy_parachraph = models.TextField(max_length=40000)
    privacy_release_date = models.DateField()

    def __str__(self):
        return self.terms_headline


class Contact_information(models.Model):
    physical_address1 = models.CharField(max_length=220)
    phone1 = models.CharField(max_length=220)
    phone2 = models.CharField(max_length=220)
    phone3 = models.CharField("Hotline", max_length=220)
    email1 = models.EmailField()
    email2 = models.EmailField()
    working_hours = models.CharField(max_length=220)
    physical_address1_arabic = models.CharField(max_length=220)
    working_hours_arabic = models.CharField(max_length=220)
    facebook_link = models.URLField()
    instagram_link = models.URLField()
    youtube_link = models.URLField()


class ContactUs(models.Model):
    name = models.CharField(max_length=255)
    mobile = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=255)
    enquiry = models.TextField(max_length=1000)
    answered = models.BooleanField(default=False)
    closed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.email

class Merchant_Request(models.Model):
    company_name = models.CharField(max_length=255)
    purchasing_manager_name = models.CharField(max_length=255)
    mobile = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=255)
    comercial_and_tax_pdf = models.FileField(upload_to="media/merchants-files", validators=[validate_file_extension])
    quotation = models.FileField(upload_to="media/merchants-files", validators=[validate_file_extension])
    supplier = models.BooleanField(default=False)
    buyer = models.BooleanField(default=False)
    answered = models.BooleanField(default=False)
    closed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.company_name
from django.db import models
from shop.models import Product
import uuid
from django.conf import settings
from django.contrib.auth import get_user_model
import datetime


class Order(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True
    )
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    email = models.EmailField(null=True, blank=False)  #false
    postal_code = models.CharField(max_length=30, blank=True)
    address = models.CharField(max_length=224, null=True)
    city = models.CharField(max_length=100)
    province = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, default="Egypt", blank=True)
    phone1 = models.CharField(null=True,max_length=12, blank=True) ################ urgently change to CharField
    phone2 = models.CharField(null=True,max_length=12, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    we_accept_transaction_id = models.CharField(max_length=2000, blank=True)
    paid = models.BooleanField(default=False)
    sent = models.BooleanField(default=False)
    cashOnDelivery = models.BooleanField(default=False)
    delivered_to_client = models.BooleanField(default=False)
    promo_code = models.CharField(max_length=150, blank=True)
    price_before_promo_code = models.CharField(max_length=150, blank=True)
    code = models.SlugField(unique=True, default=uuid.uuid1, editable=False)
    shipped = models.BooleanField(default=False)
    shipping_fees = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    fees = models.DecimalField('Total Fees',max_digits=10, decimal_places=2, null=True, blank=True)
    notes = models.TextField(max_length=4000, null=True, blank=True)

    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return "Order {}".format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

    # @property
    # def delete_after_five_minutes(self):
    #     time = self.created + datetime.timedelta(minutes=1)
    #     if (datetime.datetime.now().strftime("%b %d %Y %I %M %p") - self.created.strftime("%b %d %Y %I %M %p")) > datetime.datetime(minutes=1):
    #         e = Order.objects.get(pk=self.pk)
    #         e.delete()
    #         return True
    #     else:
    #         return False


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, related_name="order_items", on_delete=models.CASCADE
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return "product: {}, quantity: {}, price: {}".format(self.product, self.quantity, self.price)

    def get_cost(self):
        return self.price * self.quantity


class ShippingCosts(models.Model):
    shipping_city = models.CharField(max_length=50, unique=True)
    shipping_city_arabic = models.CharField(max_length=50, unique=True, null=True)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.shipping_city


class PromoCodes(models.Model):
    pormotionName = models.CharField(max_length=50, unique=True)
    discount_ratio = models.IntegerField()
    promo_code = models.CharField(max_length=50, unique=True)
    valid_from = models.DateField()
    valid_to = models.DateField()

    def __str__(self):
        return self.pormotionName
    
    class Meta:
        verbose_name_plural = "Promo Codes"
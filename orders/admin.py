from django.contrib import admin
from .models import Order, OrderItem, ShippingCosts,PromoCodes


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ('product',)
    list_display = ('product', 'quantity', 'price')
    readonly_fields = ['quantity', 'order', 'price']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'paid', 'created','shipped']
    list_filter = ['paid', 'created','shipped', 'delivered_to_client']
    inlines = [OrderItemInline, ]
    readonly_fields = ['code', 'fees', 'we_accept_transaction_id', 'paid', 'cashOnDelivery', 'promo_code', 'price_before_promo_code']
    search_fields = ['code','email', "first_name", "last_name"]

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order']


admin.site.register(Order, OrderAdmin)
admin.site.register(ShippingCosts)
admin.site.register(PromoCodes)
# admin.site.register(OrderItem, OrderItemAdmin)

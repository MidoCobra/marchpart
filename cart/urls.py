from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path(r'detail', views.cart_detail, name='cart_detail'),
    path(r'detail_arabic', views.cart_detail_arabic, name='cart_detail_arabic'),
    path(r'add/<product_id>', views.cart_add, name='cart_add'),
    path(r'add_arabic/<product_id>', views.cart_add_arabic, name='cart_add_arabic'),
    path(r'remove/<product_id>', views.cart_remove, name='cart_remove'),
    path(r'remove_arabic/<product_id>', views.cart_remove_arabic, name='cart_remove_arabic'),
    path(r'clean-cart/', views.cart_remove, name='cart_clean'),
    # url(r'^add/(?P<product_id>\d+)/$', views.cart_add, name='cart_add'),
    # url(r'^remove/(?P<product_id>\d+)/$', views.cart_remove, name='cart_remove'),
    path(r'added/<product_id>', views.AjaxAddCart, name="ajax_add_cart"),
]
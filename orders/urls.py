from django.conf.urls import url
from django.urls import path
from . import views
from main.decorators import check_recaptcha


app_name = "orders"

urlpatterns = [
    path("englishlanguage/create/", check_recaptcha(views.order_create), name="order_create"),
    path("arabiclanguage/create/", check_recaptcha(views.order_create_arabic), name="order_create_arabic"),
    path("payment/<invoice_num>/<wallet>/<path:language>", views.PayNow, name="paynow"),
    path("payment-mobile-wallet/<payment_key>", views.MobileWallet, name="WalletVodafone"),
    path(
        "we-accept/transaction-processed-callback/",
        views.ProcessesCallback,
        name="processesCallback",
    ),
    path(
        "we-accept/transaction-response-callback/",
        views.ResponseCallback,
        name="responseCallback",
    ),
    # url(r'^paypalreturn/$', views.paypal_return, name='paypal_return'),
    # url(r'^paypalcancel/$', views.paypal_cancel, name='paypal_cancel'),
]
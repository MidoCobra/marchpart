"""march URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings
from orders import views as order_views
from shop import views as shop_views
from shop_arabic import views as arabic_views
from shop_arabic.views import Home_arabic

from django.contrib.sitemaps import Sitemap
from django.contrib.sitemaps.views import sitemap
from django.contrib.sitemaps import GenericSitemap
from django.contrib.sitemaps.views import sitemap
from django.urls import path
from shop.models import Product, Blog

info_dict = {
    'queryset': Product.objects.all(),
    'date_field': 'created_at',
}


class BlogSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return Blog.objects.all()

    def lastmod(self, obj):
        return obj.created_at

class ProductSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return Product.objects.filter(hidden=False)

    def lastmod(self, obj):
        return obj.created_at

sitemaps = {
    'blog': BlogSitemap,
    'product': ProductSitemap,

}


admin.site.site_title = "March Part"
admin.site.index_title = "March Part"
admin.site.site_header = "March Part"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("users.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", Home_arabic, name="home_arabic"),
    path("cart/", include("cart.urls")),
    path("orders/", include("orders.urls")),
    path("main/", include("main.urls")),
    path("shop/arabiclanguage/", include("shop_arabic.urls")),
    path("shop/englishlanguage/", include("shop.urls")),
    re_path(r"^search/$", shop_views.search, name="search"),
    # re_path(r'^ratings/', include('star_ratings.urls', namespace='ratings', app_name='ratings')),
    re_path(
        r"^ratings/",
        include(
            "star_ratings.urls",
            namespace="ratings",
        ),
    ),
    path("api/", include("API.routers")),
    # re_path(r"api/auth/", include("djoser.urls")),
    # re_path(r"api/auth/", include("djoser.urls.authtoken")),
    re_path(r"api/v1/accounts/", include("rest_registration.api.urls")),
    # re_path(r"api/auth/", include("djoser.urls.jwt")),
    # path('api/login/', include('rest_social_auth.urls_token')), Remove with second line
    # path('api/login/', include('rest_social_auth.urls_session')),
    re_path(r'^auth/', include('drf_social_oauth2.urls', namespace='drf')),
    # re_path('', include('social_django.urls', namespace='socialDjango')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
     name='django.contrib.sitemaps.views.sitemap'),

    #     # the sitemap
    # path('sitemap.xml', sitemap,
    #      {'sitemaps': {'shop': GenericSitemap(info_dict, priority=0.6)}},
    #      name='django.contrib.sitemaps.views.sitemap'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)



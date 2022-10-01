from django.conf.urls import url
from django.urls import re_path, path
from . import views
from main.decorators import check_recaptcha


app_name = "shop_arabic"

urlpatterns = [
    # Added to main urls.py here only used for the linkin the navbar etc..
    path("", views.Home_arabic, name="home_arabic"),
    # re_path(r'^(?P<category_slug>[-\w]+)/$', views.product_list, name='product_list_by_category'),
    path(
        "all-brands-category/arabiclanguage/<category_slug>",
        views.AllBrandsCategoryProducts_arabic,
        name="all_product_list_by_category_arabic",
    ),
    # path(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.product_detail, name='product_detail'),
    path(
        "product/arabiclanguage/<id>/<slug>",
        views.product_detail_arabic,
        name="product_detail_arabic",
    ),
    path(
        "products_arabic/add-review-product/<int:product_id>",
        views.AjaxAddReviewProduct,
        name="ajax_add_review_product",
    ),
    #######################################################################
    #######################################################################
    #######################################################################
    path("models/arabiclanguage/<brandSlug>", views.ModelsView_arabic, name="models_arabic"),
    path(
        "model/arabiclanguage/categories/<modelSlug>",
        views.ModelCategories_arabic,
        name="model_categories_arabic",
    ),
    path(
        "model/category/arabiclanguage/<modelSlug>/<categorySlug>/<int:productsForAllModels>",
        views.ModelCategoryProducts_arabic,
        name="modelCategoryProducts_arabic",
    ),
    # path('model/parts/<modelSlug>', views.ModelProducts, name='model_products'),
    path("arabiclanguage/search/products", views.search_arabic, name="search_arabic"),
    path(
        "arabiclanguage/search/all-products",
        views.NavbarSearch_arabic,
        name="navbarSearch_arabic",
    ),
    path(
        "arabiclanguage/blog-details/<slug:blog_slug>",
        views.BlogDetails_arabic,
        name="blog-details_arabic",
    ),
    path(
        "arabiclanguage/blogs-by-category/<slug:blogTag_slug>",
        views.BlogByTags_arabic,
        name="blogs_by_tag_arabic",
    ),
    path("arabiclanguage/contact", check_recaptcha(views.ContactViewArabic), name="contact_arabic"),
    path("arabiclanguage/about-us", views.AboutUsArabic, name="aboutUs_arabic"),
]

# product_list_by_category

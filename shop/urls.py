from django.conf.urls import url
from django.urls import re_path, path
from . import views
from .views import ContactView
from main.decorators import check_recaptcha

app_name = "shop"

urlpatterns = [
    # Added to main urls.py here only used for the linkin the navbar etc..
    path("", views.Home, name="home"),
    # re_path(r'^(?P<category_slug>[-\w]+)/$', views.product_list, name='product_list_by_category'),
    path(
        "all-brands-category/englishlanguage/<category_slug>",
        views.AllBrandsCategoryProducts,
        name="all_product_list_by_category",
    ),
    # path(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.product_detail, name='product_detail'),
    path("product/englishlanguage/<id>/<slug>", views.product_detail, name="product_detail"),
    path(
        "products/add-review-product/<int:product_id>",
        views.AjaxAddReviewProduct,
        name="ajax_add_review_product",
    ),
    #######################################################################
    #######################################################################
    #######################################################################
    path("models/englishlanguage/<brandSlug>", views.ModelsView, name="models"),
    path(
        "model/englishlanguage/categories/<modelSlug>", views.ModelCategories, name="model_categories"
    ),
    path(
        "model/category/englishlanguage/<modelSlug>/<categorySlug>/<int:productsForAllModels>",
        views.ModelCategoryProducts,
        name="modelCategoryProducts",
    ),
    # path('model/parts/<modelSlug>', views.ModelProducts, name='model_products'),
    path("englishlanguage/search/products", views.search, name="search"),
    path("englishlanguage/search/all-products", views.NavbarSearch, name="navbarSearch"),
    path(
        "search/get-models-bybrand",
        views.Ajax_search_model_choices,
        name="ajax_search_model_choices",
    ),
    path("englishlanguage/blog-details/<slug:blog_slug>", views.BlogDetails, name="blog-details"),
    path(
        "englishlanguage/blogs-by-category/<slug:blogTag_slug>", views.BlogByTags, name="blogs_by_tag"
    ),
    path("terms-and-privacy", views.Terms, name="terms"),
    path("englishlanguage/contact", check_recaptcha(views.ContactView), name="contact"),
    path("englishlanguage/about-us", views.AboutUs, name="aboutUs"),
    path("englishlanguage/product-search-all-types", views.ProductSearchAllTypes, name="ajax_productSearchAllTypes_name"),
]

# product_list_by_category

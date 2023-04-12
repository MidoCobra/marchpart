from django.urls import include, path, re_path
from rest_framework import routers
from . import api

router = routers.DefaultRouter()
router.register(r"custom-user", api.CustomUserViewSet)
router.register(r"get-wishlist", api.WishlistViewSet)
router.register(r"add-wishlist", api.WishlistCreate)
router.register(r"models", api.ModelOfCarViewSet)
router.register(r"all-models", api.ModelOfCarViewSetNoPagination)
router.register(r"brands", api.BrandViewSet)
router.register(r"all-brands", api.BrandViewSetALL, basename="brandViewSetALL")
router.register(r"all-brands-arabic", api.BrandViewSetALLِArabic)
router.register(r"engineCapacity", api.EngineCapacityViewSet)
router.register(r"manfactureYear", api.ManfactureDateViewSet)
router.register(r"categories", api.CategoryViewSet)
router.register(r"products", api.ProductViewSet)
router.register(r"reviewProducts", api.ReviewProductViewSet)
router.register(r"homePageBanners", api.HomePage_addsViewSet)
router.register(r"homePageAdds", api.HomePage_bannersViewSet)
router.register(r"blogTags", api.Blog_tagsViewSet)
router.register(r"blogs", api.BlogViewSet)
router.register(r"last3blogs", api.LastThreeBlogsViewSet)
router.register(r"contact-us", api.ContactUSViewSet)

router.register(r"user-rating", api.UserRatingViewSet)
router.register(r"user-create-rate", api.UserRatingCreateViewSet)
router.register(r"ratings", api.RatingViewSet)

router.register(r"searchAPI", api.SearchAPI)
# router.register(r"searchByModel", api.SearchByModelAPI, basename="searchByModel")
router.register(r"filterProductsByCategory", api.FilterProductsByCategory)
router.register(r"productQueries", api.ProductQueries, basename="productQueries")

# router.register(r"promoCodes", api.PromCodeViewSet)
router.register(r"shippingCosts", api.ShippingCostsViewSet)

router.register(r"orderDetails", api.OrderViewSet)
router.register(r"orderItems", api.OrderItemViewSet)
router.register(r"order-create", api.OrderCreateViewSet)
router.register(r"orderItems-create", api.OrderItemsCreateViewSet)
router.register(r"order-update", api.OrderUPdateViewSet, basename="orderUpdate")

# router.register(r'users', api.UserViewSet)
# router.register(r'groups', api.GroupViewSet)

# router.register(
#     r"^api/auth/users/activate/(?P<uid>[\w-]+)/(?P<token>[\w-]+)/$",
#     api.UserActivationView,
# )

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    # path(
    #     "auth/users/activate/<user_id>&<timestamp>&<signature>",
    #     api.UserActivationView,
    # ),
    # re_path(
    #     r"^auth/users/activate/(?P<user_id>[\w-]+)/(?P<timestamp>[\w-]+)/(?P<signature>[\w-]+)$",
    #     api.UserActivationView,
    # ),
    path(
        "auth/users/activate/",
        api.UserActivationView,
    ),
    path(
        "auth/reset-password/",
        api.UserResetPasswordView,
    ),
    path(
        "auth/send-password/",
        api.UserGETResetPasswordView,
    ),
    # re_path(r'^order-update/$', api.OrderUPdateViewSet.as_view(), name="order-update")
    # re_path(r'^products/$', api.ProductViewSet.as_view(), name="productsAPI"),
    path('searchByModel/<str:model>/<str:manfacture_date>/<str:engine_capacity>', api.SearchByModelAPI.as_view(), name="searchByModelAPI"),
    path('promoCode/<promoCode>', api.PromCodeViewSet, name="promocodeAPI"),
    path('deleteWish/<int:id>', api.wishlist_delete_rest_endpoint, name="wishlist_delete_rest_endpoint"),
    path('update-user/<city>/<province>/<country>/<mobile>', api.customUser_edit_endpoint, name="customUser_edit_endpoint"),

    path('rate-product/<product_id>/<score>', api.customRating, name="customRating"),
]

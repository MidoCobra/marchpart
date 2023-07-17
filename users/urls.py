from django.urls import path, include, re_path
from users import views
from users import views as users_views
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from main.decorators import check_recaptcha

# from .views import UserDeleteView

# from .forms import CustomUserCreationForm, LoginForm

from rest_framework.authtoken.views import obtain_auth_token  # <-- Here

urlpatterns = [
    path(
        "accounts/password_reset/", views.password_reset_request, name="password_reset"
    ),
    path(
        "accounts/password_reset/done/",
        auth_views.PasswordResetView.as_view(template_name="password_reset_done.html"),
    ),
    path(
        # 'password_reset/confirm/<uidb64>/<token>/',
        "accounts/reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="password_reset_confirm.html"
        ),
    ),
    path(
        "accounts/reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="password_reset_complete.html"
        ),
    ),
    # path(
    #     'users/registration/',
    #     auth_views.LoginView.as_view(template_name='users/registraion/login.html'),
    # ),
    path("signup/", check_recaptcha(views.signup), name="signup"),
    path("login_arabic/", views.Login_arabic, name="login_arabic"),
    path("signup_arabic/", check_recaptcha(views.signup_arabic), name="signup_arabic"),
    # path("signup_mobile/<str:api_key>", views.Signup_Mobile_App, name="signup_mobile"),
    re_path(
        r"^account_activation_sent/$",
        views.account_activation_sent,
        name="account_activation_sent",
    ),
    re_path(
        r"^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$",
        views.activate,
        name="activate",
    ),
    ###############################################################################
    path(
        "signup/ajax/validate_username",
        views.validate_username,
        name="validate_username",
    ),
    path("signup/ajax/validate_email", views.validate_email, name="validate_email"),
    ###############################################################################
    path("User_Update", views.UpdateAccount, name="updateAccount"),
    path("Dashboard/<int:id>", views.UserDashboard, name="userDashboard"),
    path(
        "Dashboard_arabic/<int:id>",
        views.UserDashboard_arabic,
        name="userDashboard_arabic",
    ),
    path("wishlist/<int:user_id>", views.WishlistView, name="wishlistView"),
    path(
        "wishlist_arabic/<int:user_id>",
        views.WishlistView_arabic,
        name="wishlistView_arabic",
    ),
    path("ajax-wishlist/<int:product_id>", views.Ajax_Wishlist, name="ajaxWishlist"),
    path(
        "remove-item-from-wishlist/<int:product_id>",
        views.RemoveFromWishlist,
        name="removeFromWishlist",
    ),
    path(
        "remove-item-from-wishlist_arabic/<int:product_id>",
        views.RemoveFromWishlist_arabic,
        name="removeFromWishlist_arabic",
    ),
    path('user-invoices', views.UserInvoices, name='userInvoices'),
    path('user-invoices_arabic', views.UserInvoices_arabic, name='userInvoices_arabic'),
    # >>>>> SOCIAL APP LOGIN
    re_path("social-auth/", include("social_django.urls", namespace="social")),
    #     # PAYMENT VIP
    #     path('Upgrade_to_vip/<int:user_id>',
    #          views.VIP_userCreditInput, name='upgradeToVip'),
    #     re_path('FortAPIVIP/general/backToMerchant/',
    #             views.VIP_userFortAPIBackToMerchant, name='VIPFPBackMerchant'),
    #     re_path('payfort-responseV/VIPUSER/',
    #             views.VIP_userPayfortSuccess, name='VIPpayfort-response'),
    #
    ## create user Authorization Token for mobile app
    path("api-token-auth/", obtain_auth_token, name="api_token_auth"),  # <-- And here
    # path("delete-your-account", UserDeleteView.as_view(), name="delete-account")
]

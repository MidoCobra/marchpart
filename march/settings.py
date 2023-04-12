"""
Django settings for march project.

Generated by 'django-admin startproject' using Django 3.0.8.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "u5y24uar*p@)u5%18dr8)o66gyc8(npedrd8k2d=4br7eogehx"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['f76fbd57d8d9.ngrok.io','localhost', '192.168.1.11']


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # 'django.contrib.sitemaps',
    'main',
    "shop_arabic",
    "users",
    "shop",
    "cart",
    "orders",
    "API",
    "widget_tweaks",
    "social_django",
    "star_ratings",
    "rest_framework",  # install also: pip install django-filter==2.0.0
    "rest_framework.authtoken",  # <-- Here
    # 'django_filters',
    # "djoser",
    "rest_registration",
    "rest_framework_api_key",
    'import_export',
    # 'rest_social_auth', ##remove this old scosl rest auth
    'oauth2_provider',
    'drf_social_oauth2',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "march.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "cart.context_processors.cart",
                "shop.context_processors.Base",
                "social_django.context_processors.backends",  # add this
                "social_django.context_processors.login_redirect",  # add this
            ],
        },
    },
]

WSGI_APPLICATION = "march.wsgi.application"

# For CustomUser:
AUTH_USER_MODEL = "users.CustomUser"

# for social auth
LOGIN_URL = "login"
LOGOUT_URL = "logout"
# dont forget to handle this with egypt app (this is in usersapp):
LOGIN_REDIRECT_URL = "shop:home"
LOGOUT_REDIRECT_URL = "shop:home"


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'marchDatabase',
#         'USER': 'mido',
#         'PASSWORD': 'L@eba%77&him',
#         'HOST': 'localhost',
#         'PORT': '',
#     }
# }
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'march',
#         'USER': 'postgres',
#         'PASSWORD': 'lebanon&egypt',
#         'HOST': 'localhost',
#         'PORT': '',
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "EET"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
STATIC_URL = "/static/"
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
    "/shop/static",
]

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media/media")
# MEDIA_URL = 'uploaded_newsletters/

CART_SESSION_ID = "cart"
# SESSION_COOKIE_AGE = 72000
# SESSION_EXPIRE_AT_BROWSER_CLOSE = True


# EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"  ### not working
# EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"  ### not working

# EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
# EMAIL_FILE_PATH = os.path.join(BASE_DIR, "sent_emails")
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

GOOGLE_RECAPTCHA_SECRET_KEY = "6LfE570ZAAAAAOTK8AhDSgSvqMyE5RkikrfekMAl"


# FROM_EMAIL = "contact@marchpart.com"  # replace with your address
# # SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')
# SENDGRID_API_KEY = (
#     "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"
# )

# SENDGRID_API_KEY = "SG.0_NMbsbzSpG46AsIASsmPg.H2MyZuxRAAwxoAphRTuyYN3qfR237mhTM9hI3R_13iA"  ## Of DesertCamel

AUTHENTICATION_BACKENDS = [
    # 'social_core.backends.linkedin.LinkedinOAuth2',
    # 'social_core.backends.instagram.InstagramOAuth2',
    'social_core.backends.facebook.FacebookAppOAuth2',
    "social_core.backends.facebook.FacebookOAuth2",
    "social_core.backends.google.GoogleOAuth2",
    'drf_social_oauth2.backends.DjangoOAuth2',
    "django.contrib.auth.backends.ModelBackend",
]

# SOCIAL_AUTH_URL_NAMESPACE = 'socialDjango'
SOCIAL_AUTH_FACEBOOK_KEY = "1247940662205410"  # App ID
SOCIAL_AUTH_FACEBOOK_SECRET = "e12dffb204db50efaec6b8d3c70d45ec"  # App Secret
SOCIAL_AUTH_FACEBOOK_SCOPE = ["email", "user_link"]  # add this
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {  # add this
    "fields": "id, name, email, picture.type(large), link"
}
SOCIAL_AUTH_FACEBOOK_EXTRA_DATA = [  # add this
    ("name", "name"),
    ("email", "email"),
    ("picture", "picture"),
    ("link", "profile_url"),
]


REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",  # <-- And here
        # "rest_framework.authentication.SessionAuthentication",
        # "rest_framework.authentication.BasicAuthentication",
        # "rest_framework_simplejwt.authentication.JWTAuthentication",
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',  # django-oauth-toolkit >= 1.0.0
        'drf_social_oauth2.authentication.SocialAuthentication',
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
    # 'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'] i imported it in the api.py
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 4,
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
}

API_KEY_CUSTOM_HEADER = "HTTP_X_API_KEY"

# SIMPLE_JWT = {
#     "AUTH_HEADER_TYPES": ("JWT",),
# }
# SIMPLE_JWT = {
#     #   'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
#     #   'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
#     #   'ROTATE_REFRESH_TOKENS': False,
#     #   'BLACKLIST_AFTER_ROTATION': True,

#     #   'ALGORITHM': 'HS256',
#     #   'SIGNING_KEY': settings.SECRET_KEY,
#     #   'VERIFYING_KEY': None,
#     #   'AUDIENCE': None,
#     #   'ISSUER': None,

#       'AUTH_HEADER_TYPES': ('JWT',),
#     #   'USER_ID_FIELD': 'id',
#     #   'USER_ID_CLAIM': 'user_id',

#     #   'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
#     #   'TOKEN_TYPE_CLAIM': 'token_type',

#     #   'JTI_CLAIM': 'jti',

#     #   'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
#     #   'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
#     #   'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
#   }

# DJOSER = {
#     "PASSWORD_RESET_CONFIRM_URL": "password/reset/confirm/{uid}/{token}",
#     "USERNAME_RESET_CONFIRM_URL": "username/reset/confirm/{uid}/{token}",
#     "ACTIVATION_URL": "api/auth/users/activate/{uid}/{token}",
#     "SEND_ACTIVATION_EMAIL": True,
#     "SEND_CONFIRMATION_EMAIL": True,
#     "LOGIN_FIELD": "email",
#     # "HIDE_USERS": True,
#     "SERIALIZERS": {
#         "user_create": "API.serializers.CustomUserCreateSerializer",
#         "user": "API.serializers.CustomUserSerializer",
#         "user_delete": "API.serializers.CustomUserSerializer",
#         "activation": "djoser.email.ActivationEmail",
#     },
# }


REST_REGISTRATION = {
    "REGISTER_VERIFICATION_ENABLED": True,
    "RESET_PASSWORD_VERIFICATION_ENABLED": True,
    "REGISTER_EMAIL_VERIFICATION_ENABLED": True,
    "RESET_PASSWORD_VERIFICATION_URL": True,
    "REGISTER_VERIFICATION_URL": "https://127.0.0.1:8000/api/auth/users/activate/",
    # "REGISTER_VERIFICATION_URL": "https://127.0.0.1:8000/verify-user/",
    "RESET_PASSWORD_VERIFICATION_URL": "https://127.0.0.1:8000/api/auth/reset-password/",
    "REGISTER_EMAIL_VERIFICATION_URL": "https://127.0.0.1:8000/api/auth/verify-email/",
    "VERIFICATION_FROM_EMAIL": "contact@marchpart.com",
}


OAUTH2_PROVIDER = {
    # 'SCOPES': {
    #     'read': 'Read scope',
    #     'write': 'Write scope',
    # },

    'ACCESS_TOKEN_EXPIRE_SECONDS': 1800000000,

}

# DRFSO2_PROPRIETARY_BACKEND_NAME: "Djangoz"
ACTIVATE_JWT = False
# ## sendgrid email service
# EMAIL_HOST = "smtp.sendgrid.net"
# EMAIL_PORT = 587
# # EMAIL_HOST_USER = "desertcamel"
# # EMAIL_HOST_PASSWORD = "egy&mido&2010"
# EMAIL_USE_TLS = True

EMAIL_BACKEND = "sendgrid_backend.SendgridBackend"
# SERVER_EMAIL = "contact@marchpart.com"
## sendgrid email service
EMAIL_HOST = "smtp.sendgrid.net"
# EMAIL_PORT = 587
EMAIL_PORT = 465
EMAIL_HOST_USER = "michael.fahim@marchpart.com"
EMAIL_HOST_PASSWORD = "123mmm@@@"
# EMAIL_USE_TLS = True
EMAIL_USE_SSL = True
FROM_EMAIL = "contact@marchpart.com"  # replace with your address
# SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')
SENDGRID_API_KEY = (
    "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"
)


FILE_UPLOAD_HANDLERS = ("django_excel.ExcelMemoryFileUploadHandler",
                        "django_excel.TemporaryExcelFileUploadHandler")
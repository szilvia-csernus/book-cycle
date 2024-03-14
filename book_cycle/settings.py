"""
Django settings for book_cycle project.

Generated by 'django-admin startproject' using Django 3.2.20.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from decimal import Decimal
from pathlib import Path
import os
import dj_database_url
from dotenv import load_dotenv
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = "DEBUG" in os.environ

ALLOWED_HOSTS = ['book-cycle-f6aff45df7ba.herokuapp.com', 'localhost',
                 '127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',  # also needed for allauth
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',  # also needed for allauth
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # for allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',

    # my apps
    'home',
    'inventory',
    'shopping_bag',
    'orders',
    'profiles',
    'storages',

    # other
    'crispy_forms',
    'pwa',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'book_cycle.urls'

CRISPY_TEMPLATE_PACK = 'uni_form'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                # for  {{ MEDIA_URL }}noimage.png format to work
                'django.template.context_processors.media',

                # `allauth` needs this from django
                'django.template.context_processors.request',

                # context for subjects, yeargroups, shopping bag and order
                # details to be available throughout the pages
                'inventory.context.all_categories',
                'shopping_bag.context.bag_contents',
                'orders.context.manage_orders_details',
            ],
            'builtins': [
                'crispy_forms.templatetags.crispy_forms_tags',
                'crispy_forms.templatetags.crispy_forms_field',
            ]
        },
    },
]

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

WSGI_APPLICATION = 'book_cycle.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

if 'DATABASE_URL' in os.environ:
    DATABASES = {
        'default': dj_database_url.parse(os.environ.get('DATABASE_URL', ''))
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
 {'NAME':
  'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
  },
 {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
  },
 {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
  },
 {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
  },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/London'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'), )

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# for allauth
AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend'
]

# for allauth
SITE_ID = 1
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
# The default behaviour is not log users in and to redirect them to
# ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL.
# By changing this setting to True, users will automatically be logged in
# once they confirm their email address. Note however that this only works
# when confirming the email address immediately after signing up,
# assuming users didn’t close their browser or used some sort of
# private browsing mode.
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_LOGIN_ON_PASSWORD_CHANGE = True
ACCOUNT_LOGIN_ON_PASSWORD_RESET = True
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_FORMS = {'signup': 'profiles.forms.CustomSignupForm'}
ACCOUNT_SIGNUP_VIEW = 'profiles.views.CustomSignupView'
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        # For each OAuth based provider, either add a ``SocialApp``
        # (``socialaccount`` app) containing the required client
        # credentials, or list them here:
        'APP': {
            'client_id': os.environ.get('GOOGLE_CLIENT_ID'),
            'secret': os.environ.get('GOOGLE_SECRET'),
            'key': ''
        },
        # These are provider-specific settings that can only be
        # listed here:
        'SCOPE': [
            'profile',
            'email'
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    },
    'facebook': {
        'APP': {
            'client_id': os.environ.get('FACEBOOK_CLIENT_ID'),
            'secret': os.environ.get('FACEBOOK_SECRET'),
            'key': ''
        },
        'METHOD': 'js_sdk',
        'SDK_URL': '//connect.facebook.net/{locale}/sdk.js',
        'SCOPE': ['email', 'public_profile'],
        'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
        'INIT_PARAMS': {'cookie': False},
        'FIELDS': [
            'id',
            'first_name',
            'last_name'
        ],
        'VERIFIED_EMAIL': True,
        'VERSION': 'v18.0',
        'GRAPH_API_URL': 'https://graph.facebook.com/v18.0',
    }
}
SOCIALACCOUNT_EMAIL_AUTHENTICATION = True
SOCIALACCOUNT_LOGIN_ON_GET = True
SOCIALACCOUNT_QUERY_EMAIL = True
SOCIALACCOUNT_EMAIL_AUTHENTICATION_AUTO_CONNECT = True
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

ACCOUNT_CHANGE_PASSWORD_REDIRECT_URL = '/profiles/profile/'
ACCOUNT_PASSWORD_RESET_REDIRECT_URL = '/profiles/profile/'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

TEST_RUNNER = "redgreenunittest.django.runner.RedGreenDiscoverRunner"

STRIPE_CURRENCY = 'gbp'
STRIPE_PUBLIC_KEY = os.getenv('STRIPE_PUBLIC_KEY', '')
STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY', '')
STRIPE_WH_SECRET = os.getenv('STRIPE_WH_SECRET', '')

SHIPPING_COST = Decimal(3.50)

# AWS S3
if 'USE_AWS' in os.environ:
    # Cache control
    AWS_S3_OBJECT_PARAMETERS = {
        'Expires': 'Thu, 31 Dec 2099 20:00:00 GMT',
        'CacheControl': 'max-age=94608000',
        }

    AWS_STORAGE_BUCKET_NAME = 'book-cycle'
    AWS_S3_REGION_NAME = 'eu-west-2'
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'

    # Static and media files
    STATICFILES_STORAGE = 'custom_storages.StaticStorage'
    STATICFILES_LOCATION = 'static'
    DEFAULT_FILE_STORAGE = 'custom_storages.MediaStorage'
    MEDIAFILES_LOCATION = 'media'

    # Override static and media URLs in production
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{STATICFILES_LOCATION}/'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{MEDIAFILES_LOCATION}/'

if 'DEVELOPMENT' in os.environ:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    DEFAULT_FROM_EMAIL = 'bookCYCLE@example.com'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_USE_TLS = True
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASS')
    DEFAULT_FROM_EMAIL = os.environ.get('EMAIL_HOST_USER')
    EMAIL_PORT = 587
    SERVER_EMAIL = os.environ.get('EMAIL_HOST_USER')

ADMINS = [('Admin', os.environ.get('EMAIL_HOST_USER'))]


# PWA
PWA_SERVICE_WORKER_PATH = os.path.join(BASE_DIR, 'home', 'serviceworker.js')
PWA_APP_NAME = 'BookCycle'
PWA_APP_DESCRIPTION = "All-condition webshop for secondary schools in the UK."
PWA_APP_THEME_COLOR = '#560190'
PWA_APP_BACKGROUND_COLOR = '#560190'
PWA_APP_DISPLAY = 'standalone'
PWA_APP_SCOPE = '/'
PWA_APP_ORIENTATION = 'any'
PWA_APP_START_URL = '/'
PWA_APP_STATUS_BAR_COLOR = 'default'
PWA_APP_ICONS = [
    {
        "src": os.path.join(STATIC_URL, "icons/android-chrome-192x192.png"),
        "sizes": "192x192",
        "type": "image/png"
    },
    {
        "src": os.path.join(STATIC_URL, "icons/android-chrome-512x512.png"),
        "sizes": "512x512",
        "type": "image/png",
        "purpose": "maskable",
    },
    {
        "src": os.path.join(STATIC_URL, "icons/android-chrome-512x512.png"),
        "sizes": "512x512",
        "type": "image/png",
        "purpose": "any",
    }
]
PWA_APP_ICONS_APPLE = [
    {
        'src': os.path.join(STATIC_URL, 'icons/apple-touch-icon.png'),
        'sizes': '160x160'
    }
]
PWA_APP_SPLASH_SCREEN = [
    {
        'src': os.path.join(STATIC_URL,
                            "screenshots/landing-page-light-mobile.jpeg"),
        'media': '(device-width: 320px) and (device-height: 568px) \
        and (-webkit-device-pixel-ratio: 2)'
    }
]
PWA_APP_DIR = 'ltr'
PWA_APP_LANG = 'en-US'
PWA_APP_SCREENSHOTS = [
    {
        "src": os.path.join(STATIC_URL,
                            "screenshots/landing-page-light-mobile.jpeg"),
        "sizes": "348x752",
        "type": "image/png",
        "form_factor": "narrow"
    },
    {
        "src": os.path.join(STATIC_URL,
                            "screenshots/books-light.jpeg"),
        "sizes": "884x857",
        "type": "image/png",
        "form_factor": "wide"
    }
]
PWA_APP_DEBUG_MODE = False

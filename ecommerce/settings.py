"""
Django settings for ecommerce project.

Generated by 'django-admin startproject' using Django 3.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
from pathlib import Path
from django.utils.translation import gettext_lazy as _  #for multi languanges

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'mst6!yv6=eez559kkbgsw8ui30j$9eoc-7&a41e*7nx)z&w&bt'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    'localhost'
    #'127.0.0.1' # for local host
   # 'mydjangoajax.herokuapp.com' # add for heroku domain name
    

]


# Application definition


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize', # for install filter templatage '1000.05' to '1,000.05'
    'home',
    'products',
    'order',
    'user',
    'vendors',
    'ckeditor',
    'mptt', # django-mptt for Category 
    'import_export',
    'coupons',
    'wishlist', # for wish list or favorit products lsit
    'django_simple_coupons', #install package django simple coupons
    'debug_toolbar', # debug toolbar package
    # install the socialmedia login
    'django.contrib.sites',
    #install socialmedia login
    #allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    #install socialmedia login
    # ... include the providers you want to enable:
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.twitter',
    'allauth.socialaccount.providers.telegram',
    #for Google ReCapchar i'm not robot
    'django_recaptcha',
    #'captcha',
    #for 'crispy_forms',
    'crispy_forms',
    # install tweads to add class
    'widget_tweaks',
    # phonefield for phone number 
    'phonenumber_field',
    # generate QR code 
    'qr_code', 
    # for tags products
    'taggit',# pip install django-taggit==3.1.0
    #'tagging', not working


]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',       # add deploy
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware', # for multilanguage
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware', # for debug toolbar
]

ROOT_URLCONF = 'ecommerce.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # `allauth` needs this from django
                # 'django.template.context_processors.request',
               # 'apps.store.context_processores.menu_categories',
                #'apps.store.context_processores.globle_main_menus',
                #'apps.store.context_processores.globle_sub_menus1',
                'wishlist.context_processors.wishsession', # for apply wish session all page
                'order.context_processors.cartsession', # for apply Cart session all page
            ],
        },
    },
]

WSGI_APPLICATION = 'ecommerce.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/
#for multi language
# Provide a lists of languages which your site supports.
LANGUAGES = [
    ('km', _('Khmer')),  #km for khmer language
    ('en', _('English')),
]

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

# Default languages
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Bangkok'


USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

IMPORT_EXPORT_USE_TRANSACTIONS=True


STATIC_URL = '/static/'

# for pdf print
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')   # original

#STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')                      #add for deploy


# create path for folder upload
MEDIA_URL='/media/'
MEDIA_ROOT= os.path.join(BASE_DIR,'uploads/')

#... Copy the ckeditor from its'website link
SITE_ID = 1

####################################
    ##  CKEDITOR CONFIGURATION ##
####################################

CKEDITOR_JQUERY_URL = 'https://ajax.googleapis.com/ajax/libs/jquery/2.2.4/jquery.min.js'

CKEDITOR_UPLOAD_PATH = 'ckimages/'
CKEDITOR_IMAGE_BACKEND = "pillow"

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': None,
    },
}

###################################

# message tag alert for bootstrap
from django.contrib.messages import constants as messages
MESSAGE_TAGS={
    messages.DEBUG:'alert-info',
    messages.INFO:'alert-info',
    messages.SUCCESS:'alert-success',
    messages.WARNING:'alert-warning',
    messages.ERROR:'alert-danger',
}

#install socialmedia login
SITE_ID = 1
#install socialmedia login after login it will direct to from page
LOGIN_REDIRECT_URL = "/"

#forgooglelogin Scoop
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
    },
    'facebook': {
           'SCOPE': ['email'],  #, 'publish_stream'],
           'METHOD': 'oauth2'  # 'js_sdk'  # instead of 'oauth2'
       },
    'telegram': {
            'TOKEN': 'insert-token-received-from-botfather'
        },
}
# socialmedia allauth required
#for sending email contactus.html emailsetting
#EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'tengsamak@gmail.com' #sender email-id your email account
EMAIL_HOST_PASSWORD = 'xuol jvia dthn wyoo' #password associated with sender email-id your email encrip pass
#end sending email

# install socialmedia required
AUTHENTICATION_BACKENDS = [
    # ...
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
    # ...
]
#allauth want to collect user info required
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'

#for debug toolbar ip
INTERNAL_IPS = [
    # ...
    
    '127.0.0.1',
    # ...
]

# For reCapcha
RECAPTCHA_PUBLIC_KEY = '6LeBti8pAAAAAMYVX1AHQNvqIxNO7e5jMxKq_p0M'
RECAPTCHA_PRIVATE_KEY = '6LeBti8pAAAAALaK4X84WTKhuWyyaiC2xljYSNoa'
SILENCED_SYSTEM_CHECKS = ['django_recaptcha.recaptcha_test_key_error']

#RECAPTCHA_DOMAIN = 'www.recaptcha.net'
#RECAPTCHA_PROXY = {'http': 'http://127.0.0.1:8000', 'https': 'https://127.0.0.1:8000'}

RECAPTCHA_REQUIRED_SCORE = 0.85

#for allow host use
#ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'www.sommarmart.com']
ALLOWED_HOSTS = []

#for crispy form
#CRISPY_TEMPLATE_PACK = 'uni_form'

# for expired token sent via email
#PASSWORD_RESET_TIMEOUT=86400 # 24h in second
PASSWORD_RESET_TIMEOUT_DAYS=1
AUTH_TOKEN_VALIDITY=1

#for upgrate from django 3.1 to 3.2
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# info for Telegram TOKEN when sent to group
TOKEN="7043199444:AAGRP4Uo25wOHY6_7Y-rbtWCV-iTxGMDPUg"
CHAT_ID="-4159721907"
# end info
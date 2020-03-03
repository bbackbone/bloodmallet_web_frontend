"""
Django settings for bloodmallet project.

Generated by 'django-admin startproject' using Django 2.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',     # required by django-allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.patreon',
    'sass_processor',
    'corsheaders',
    'crispy_forms',
    'vinaigrette',
    'general_website.apps.GeneralWebsiteConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'vinaigrette.middleware.VinaigretteAdminLanguageMiddleware',
]

try:
    import compute_api
except ModuleNotFoundError:
    pass
else:
    INSTALLED_APPS.append('compute_api.apps.ComputeApiConfig')
    MIDDLEWARE.append('compute_api.broadcast_middleware.BroadcastMiddleware')

ROOT_URLCONF = 'bloodmallet.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'general_website', 'templates', 'allauth')     # allauth templates
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.i18n',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'bloodmallet.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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

try:
    from .secrets import SECRET_KEY
except ModuleNotFoundError:
    from django.core.management.utils import get_random_secret_key
    SECRET_KEY = get_random_secret_key()

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'sass_processor.finders.CssFinder',
]

# TODO: Check https://django-allauth.readthedocs.io/en/latest/faq.html for patreon connection
# django-allauth
AUTHENTICATION_BACKENDS = (
     # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

     # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)
# allauth
SITE_ID = 1
# ACCOUNT_ADAPTER = 'general_website.allauth_overwrite.SocialAccountAdapter'

# we can either use crispy or bootstrap4
CRISPY_TEMPLATE_PACK = 'bootstrap4'     # automatic bootstrap form frontend generator

# from where is this?
LOGIN_URL = 'login'

# replaces the Django standard User
AUTH_USER_MODEL = 'general_website.User'

LOCALE_PATHS = (BASE_DIR + '/general_website/locale',)

try:
    from bloodmallet.settings.secrets import PROJECT, ZONE, CPU_TYPE, IMAGE_FAMILY, FALLBACK_ZONE
except ModuleNotFoundError:
    # information is not required for local development of the frontend
    pass
else:
    # Google cloud storage handling
    DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'

STANDARD_CHART_NAME = 'Bloodmallet Standard Chart'

# adjust messages tags to match bootstrap
from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

# try to fix the cors issue for the downloader
CORS_ORIGIN_ALLOW_ALL = True
CORS_URLS_REGEX = r'^/chart/get/.*$'
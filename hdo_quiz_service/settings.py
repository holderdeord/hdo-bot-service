"""
Django settings for hdo_quiz_service project.

Generated by 'django-admin startproject' using Django 1.10.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import dj_database_url
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 's%4#6c-2x1-4b-xgwp=6@+)9&i-bknua0li4nlsn)@g=04^upk')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG') in ('1', 'true', 'True')

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')

# Application definition
REMOTE_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'rest_framework',
    'corsheaders',
]

LOCAL_APPS = [
    'api',
    'messenger_bot',
    'quiz',
]

INSTALLED_APPS = REMOTE_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'hdo_quiz_service.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'hdo_quiz_service.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

database_config = dj_database_url.config()
if database_config:
    DATABASES['default'] = database_config


# Test settings
TEST_RUNNER = 'hdo_quiz_service.runners.PytestTestRunner'

# Logging
# https://docs.djangoproject.com/en/1.10/ref/settings/#logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('LOG_LEVEL', 'INFO'),
        },
        'django.db': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_DB_LOG_LEVEL', 'WARNING'),
            'propagate': False,
        }
    },
    'root': {
        'handlers': ['console'],
        'level': os.getenv('LOG_LEVEL', 'DEBUG'),
        'propagate': False,
    },

}

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = os.getenv('TIME_ZONE', 'UTC')
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

# Facebook/Messenger
FACEBOOK_APP_ACCESS_TOKEN = os.getenv('FACEBOOK_APP_ACCESS_TOKEN')
FACEBOOK_APP_VERIFICATION_TOKEN = os.getenv('FACEBOOK_APP_VERIFICATION_TOKEN', 'thisismadness')
FACEBOOK_APP_ID = os.getenv('FACEBOOK_APP_ID')
FACEBOOK_PAGE_ID = os.getenv('FACEBOOK_PAGE_ID')


# Google import
GOOGLE_OAUTH2_CLIENT_ID = os.getenv('GOOGLE_OAUTH2_CLIENT_ID', 'DUMMY')
GOOGLE_OAUTH2_CLIENT_SECRET = os.getenv('GOOGLE_OAUTH2_CLIENT_SECRET', 'DUMMY')
GOOGLE_OAUTH2_SCOPES = ('https://www.googleapis.com/auth/spreadsheets.readonly',)
GOOGLE_OAUTH2_STORAGE_MODEL = {
    'model': 'quiz.models.GoogleProfile',
    'user_property': 'user',
    'credentials_property': 'credential',
}
GOOGLE_SPREADSHEET_ID = os.getenv('GOOGLE_SPREADSHEET_ID')

CORS_ORIGIN_ALLOW_ALL = True

try:
    from .local_settings import *  # noqa
except ImportError:
    pass  # All good!

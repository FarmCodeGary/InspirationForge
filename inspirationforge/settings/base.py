"""
Django settings for inspirationforge project.

Generated by 'django-admin startproject' using Django 1.8.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

import dj_database_url

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))


SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {'default':  dj_database_url.config()}


# E-mail settings
DEFAULT_FROM_EMAIL = os.environ["DJANGO_DEFAULT_FROM_EMAIL"]
SERVER_EMAIL = os.environ["DJANGO_SERVER_EMAIL"]
EMAIL_HOST = os.environ["DJANGO_EMAIL_HOST"]
EMAIL_PORT = os.environ["DJANGO_EMAIL_PORT"]
EMAIL_HOST_USER = os.environ["DJANGO_EMAIL_HOST_USER"]
EMAIL_HOST_PASSWORD = os.environ["DJANGO_EMAIL_HOST_PASSWORD"]
EMAIL_USE_SSL = (os.environ["DJANGO_EMAIL_USE_SSL"] == 'true')
EMAIL_SUBJECT_PREFIX = "[Inspiration Forge] "


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'blog',
    'bootstrap3',
    'storages',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'inspirationforge.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'blog.context_processors.latest_content',
            ],
        },
    },
]

WSGI_APPLICATION = 'inspirationforge.wsgi.application'


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/Detroit'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Sites framework
SITE_ID = 1


MEDIA_URL = "/media/"

ADMINS = ((os.environ["DJANGO_ADMIN_NAME"], os.environ["DJANGO_ADMIN_EMAIL"]),)

"""
Django settings for imagr_site project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from configurations import Configuration, values


BASE_DIR = os.path.dirname(os.path.dirname(__file__))


class Base(Configuration):
    TIME_ZONE = 'America/Los_Angeles'
    LANGUAGE_CODE = 'en-us'

    USE_I18N = True

    USE_L10N = True

    USE_TZ = True

    STATIC_URL = '/static/'

    MEDIA_ROOT = BASE_DIR + "/media/"

    PHOTO_URL = '/photo/'
    ALBUM_URL = '/album/'
    MEDIA_URL = '/media/'

    ALLOWED_HOSTS = []

    AUTH_USER_MODEL = 'imagr_users.ImagrUser'

    ROOT_URLCONF = 'imagr_site.urls'

    WSGI_APPLICATION = 'imagr_site.wsgi.application'

    # DJANGO_SECRET_KEY = values.SecretValue()
    SECRET_KEY = values.SecretValue()

    MIDDLEWARE_CLASSES = (
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    )

    INSTALLED_APPS = (
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'imagr_users',
        'imagr_images',
        'south',
    )


class Dev(Base):
    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = values.BooleanValue(True)
    TEMPLATE_DEBUG = values.BooleanValue(True)
    SECRET_KEY = 'thisisecret'

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }


class Prod(Base):
    TIME_ZONE = 'UTC'
    DEBUG = False
    TEMPLATE_DEBUG = False

    SECRET_KEY = values.SecretValue(environ_name='SECRET_KEY')

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': values.SecretValue(enivron_name='IMAGR_DB_NAME'),
            'USER': values.SecretValue(environ_name='IMAGR_DB_USER'),
            'PASSWORD': values.SecretValue(environ_name='IMAGR_DB_PASSWORD'),
            'HOST': values.SecretValue(environ_name='IMAGR_DB_HOST')
        }
    }

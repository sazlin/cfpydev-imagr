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

    MEDIA_ROOT = BASE_DIR + "/media/"

    PHOTO_URL = '/photo/'
    ALBUM_URL = '/album/'
    MEDIA_URL = '/media/'
    STATIC_URL = '/static/'

    ALLOWED_HOSTS = [values.Value('didnt work', environ_name='IMAGR_HOST')]
    STATIC_ROOT = os.path.join(BASE_DIR, "static/")
    AUTH_USER_MODEL = 'imagr_users.ImagrUser'

    ROOT_URLCONF = 'imagr_site.urls'

    WSGI_APPLICATION = 'imagr_site.wsgi.application'

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

    TEMPLATE_LOADERS = (
            ('django.template.loaders.cached.Loader', (
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader', )),
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
    MEDIA_URL = '/media/'
    MEDIA_ROOT = '/home/ubuntu/media'
    TIME_ZONE = 'UTC'
    DEBUG = True
    TEMPLATE_DEBUG = True
    CSRF_COOKIE_SECURE = False  # should turn this on
    SESSION_COOKIE_SECURE = False  # should turn this on
    CONN_MAX_AGE = 10
    SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ.get('DJANGO_IMAGR_DB_NAME'),
            'USER': os.environ.get('DJANGO_IMAGR_DB_USER'),
            'PASSWORD': os.environ.get('DJANGO_IMAGR_DB_PASSWORD'),
            'HOST': os.environ.get('DJANGO_IMAGR_DB_HOST'),
        }
    }

"""
Django settings for axisapp project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""
import logging
import os
import sys
from urlparse import urlparse

DJ_DIR = os.path.dirname(__file__)
BASE_DIR = os.path.dirname(DJ_DIR)

VERSION = '0.0.1-genesis'

ON_CI = 'CIDONKEY' in os.environ
MIG_TESTS = 'MIG_TEST' in os.environ
TESTING = any(word in sys.argv for word in ('test', 'fast_test', 'selenium_test')) or MIG_TESTS

ADMINS = (('Dairon Medina', 'info@gydsystems.com'),
          ('Testing', 'axis-app-testing@gmail.com'))
MANAGERS = ADMINS
INTERNAL_IPS = ('localhost', '127.0.0.1')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '%9#uh5vjsa09oev@_#&&=efj1wl6i1i7*-i!lhx9*tofxmq$-!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #Third party
    'django_jinja',
    'storages',
    #Axis
    'axisapp.core',
    'axisapp.company',
    'axisapp.security',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.core.context_processors.request',
    'django.core.context_processors.csrf',
    'django.contrib.messages.context_processors.messages',
)


TEMPLATE_LOADERS = (
    'django_jinja.loaders.FileSystemLoader',
    'django_jinja.loaders.AppLoader'
)

DEFAULT_JINJA2_TEMPLATE_EXTENSION = '.jinja'

JINJA2_ENVIRONMENT_OPTIONS = {
    'trim_blocks': True,
}

TEMPLATE_DIRS = (
    os.path.join(DJ_DIR, 'templates'),
)

AUTH_USER_MODEL = 'security.User'
AUTHENTICATION_BACKENDS = ('axisapp.security.backends.CompanyModelBackend',)

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

STATICFILES_DIRS = (os.path.join(DJ_DIR, 'static'),)

# Use Amazon S3 for managing statics
USE_S3 = False

ROOT_URLCONF = 'axisapp.urls'

WSGI_APPLICATION = 'axisapp.wsgi.application'


# setup for sentry
if not DEBUG:
    RAVEN_CONFIG = {
        'dsn': os.environ.get('RAVEN_DSN'),
    }


redis_url = urlparse(os.getenv('REDISCLOUD_URL', 'redis://localhost:6379'))
CACHES = {
    'default': {
        'BACKEND': 'redis_cache.cache.RedisCache',
        'LOCATION': '%s:%s:0' % (redis_url.hostname, redis_url.port),
        'OPTIONS': {
            'CLIENT_CLASS': 'redis_cache.client.DefaultClient',
            'PASSWORD': redis_url.password,
            'CONNECTION_POOL_KWARGS': {'max_connections': 10}
        }
    }
}



# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

if DEBUG and not ON_CI and not TESTING:
    # https://github.com/django-debug-toolbar/django-debug-toolbar/issues/497
    MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware', )
    INSTALLED_APPS += ('debug_toolbar.apps.DebugToolbarConfig',)
    DEBUG_TOOLBAR_PANELS = [
        'debug_toolbar.panels.versions.VersionsPanel',
        'debug_toolbar.panels.timer.TimerPanel',
        'debug_toolbar.panels.settings.SettingsPanel',
        'debug_toolbar.panels.headers.HeadersPanel',
        'debug_toolbar.panels.request.RequestPanel',
        'debug_toolbar.panels.sql.SQLPanel',
        'debug_toolbar.panels.staticfiles.StaticFilesPanel',
        'debug_toolbar.panels.templates.TemplatesPanel',
        'debug_toolbar.panels.cache.CachePanel',
        'debug_toolbar.panels.signals.SignalsPanel',
        'debug_toolbar.panels.logging.LoggingPanel',
        'debug_toolbar.panels.profiling.ProfilingPanel',
        'debug_toolbar.panels.redirects.RedirectsPanel',
    ]

    # TODO: this is unsafe and needs fixing before launch
    DEBUG_TOOLBAR_CONFIG = {
        'SHOW_TOOLBAR_CALLBACK': "%s.is_auth" % __name__,
    }

    def is_auth(request):
        return request.user.is_authenticated()

# whether super admins can log in to an agency.
SUPER_ADMIN_AGENCY_ACCESS = True

# New Company created in inactive state
COMPANY_NEEDS_APPROVAL = True

# Send emails to settings.ADMINS when new Company is created
NOTIFY_ADMINS_ON_NEW_COMPANY = COMPANY_NEEDS_APPROVAL

# whether ot not to run migrations during testing, should be true here
# but can be switched in localsettings.py
TEST_MIGRATIONS = True

# number of processes to use during testing, if 1 testing is vanilla django,
# otherwise concurrency test is used.
TEST_CONCURRENCY = 1

# Auto LogOut user after 2 hours of inactivity
SESSION_SAVE_EVERY_REQUEST = True
SESSION_COOKIE_AGE = 2 * 60 * 60

# CAPTCHA_CHALLENGE_FUNCT = 'captcha.helpers.math_challenge'
CAPTCHA_FONT_SIZE = 40
CAPTCHA_LETTER_ROTATION = (-30, 30)
CAPTCHA_NOISE_FUNCTIONS = ('captcha.helpers.noise_arcs', 'captcha.helpers.noise_dots',)

# as a rule we will only use S3 when the system is actually running on production
if USE_S3:
    # these are the "default" settings used for private files
    AWS_QUERYSTRING_AUTH = True
    AWS_S3_SECURE_URLS = True
    AWS_DEFAULT_ACL = 'private'
    # AWS_QUERYSTRING_EXPIRE = 600

    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', '')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', '')
    AWS_STORAGE_BUCKET_NAME = 'axisapp-private'

    MEDIA_URL = 'https://s3-eu-west-1.amazonaws.com/axisapp-private/'

    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

    PUBLIC_URL = 'https://axisapp-public.s3.amazonaws.com/'
    PUBLIC_AWS_STORAGE_BUCKET_NAME = 'tutorcruncher-public'
    PUBLIC_AWS_HEADERS = {"Cache-Control": "public, max-age=86400", }
    PUBLIC_AWS_QUERYSTRING_AUTH = False
    PUBLIC_AWS_DEFAULT_ACL = 'public-read'

    STATIC_URL = 'https://axisapp.s3.amazonaws.com/'
    STATIC_AWS_STORAGE_BUCKET_NAME = 'axisapp'
    STATIC_AWS_HEADERS = {"Cache-Control": "public, max-age=86400", }
    STATIC_AWS_QUERYSTRING_AUTH = False
    STATIC_AWS_DEFAULT_ACL = 'public-read'

    STATICFILES_STORAGE = 'axisapp.storage.StaticStorage'

    # AWS_REDUCED_REDUNDANCY = False
    AWS_IS_GZIPPED = False
else:
    STATIC_ROOT = 'staticfiles'
    STATIC_URL = '/static/'

    MEDIA_ROOT = 'mediafiles'
    MEDIA_URL = '/media/'

    PUBLIC_URL = '/media/public/'

# You can use this to locate slowest tests:
# > pip install django-slowtests
# TEST_RUNNER = 'django_slowtests.DiscoverSlowestTestsRunner'

# this provides a way of overwriting variables locally without
# adding it to git, use for TEST_MIGRATIONS, TEST_CONCURRENCY, DATABASES
try:
    from localsettings import *
except ImportError:
    pass
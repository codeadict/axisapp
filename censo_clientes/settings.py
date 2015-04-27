"""
Django settings for censo_clientes project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import datetime
import djcelery

djcelery.setup_loader()
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '7g*s8f0em%9!08kbrm4nqcdg%b!a1@rg(j&j#&h=6rrftlg+y2'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    #'suit',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'cacheops',
    'bootstrapform_jinja',
    'bootstrap3_datetime',
    'django_jinja',
    'django_jinja.contrib._easy_thumbnails',
    'djcelery',
    'rest_framework',
    'smart_selects',
    'leaflet',
    'djgeojson',
    'import_export',
    'account',
    'sdauth',
    'easy_thumbnails',
    'base',
    'censo',
    'corsheaders',
    #For countries fields
    #'django-countries',
    #For python-mptt
    'mptt',
    'hhrr',
    'products'
)

SILENCED_SYSTEM_CHECKS = ['auth.W004']

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.SHA1PasswordHasher',
    'django.contrib.auth.hashers.MD5PasswordHasher',
    'django.contrib.auth.hashers.CryptPasswordHasher',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'sdauth.middleware.SDAuthMiddleware',
)


TEMPLATE_LOADERS = (
    'django_jinja.loaders.FileSystemLoader',
    'django_jinja.loaders.AppLoader'
)

DEFAULT_JINJA2_TEMPLATE_EXTENSION = '.jinja'

JINJA2_MUTE_URLRESOLVE_EXCEPTIONS = DEBUG
# Same behavior of default intercept method
# by extension but using regex (not recommended)
DEFAULT_JINJA2_TEMPLATE_INTERCEPT_RE = r'.*jinja$'

# More advanced method. Intercept all templates
# except from django admin.
#DEFAULT_JINJA2_TEMPLATE_INTERCEPT_RE = r"^(?!admin/).*"

JINJA2_ENVIRONMENT_OPTIONS = {
    'trim_blocks': True,
}

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

    'base.context.app_basic',
)

ROOT_URLCONF = 'censo_clientes.urls'

WSGI_APPLICATION = 'censo_clientes.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'axisapp',
        'USER': 'postgres',
        'PASSWORD': 'swda-1432',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'es-es'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)
STATIC_ROOT = os.path.join(BASE_DIR, 'static_serv')

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MEDIA_URL = '/media/'

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

APK_FILE_STORAGE_PATH = os.path.join(MEDIA_ROOT, 'android')

SUIT_CONFIG = {
    'SEARCH_URL': '/censo/cliente/',
    'MENU_EXCLUDE': ('auth.group',),
    'MENU_ICONS': {
        'base': 'icon-cog',
        'censo': 'icon-map-marker',
        'auth': 'icon-user',
    },
    'ADMIN_NAME': 'Sistema de Distribucion',
    'MENU': (
        {'label': 'Clientes', 'icon': 'icon-map-marker', 'models': [
            {'label': 'Datos de Clientes', 'url': 'censo.cliente'},
            {'label': 'Mapa', 'url': 'mapa'}
        ]},
        {'app': 'base', 'label': 'Datos Maestros', 'icon': 'icon-cog'},
        {'app': 'auth', 'label': 'Seguridad', 'icon': 'icon-lock'},
        {'label': 'Descargar App Android', 'url': 'apkdown', 'icon': 'icon-download-alt', 'blank': True},
    )
}


# mapa

LEAFLET_CONFIG = {
    'DEFAULT_CENTER': (0.2298500, -78.5249500),
    'DEFAULT_ZOOM': 7,
    'MIN_ZOOM': 3,
    'MAX_ZOOM': 18,

    'PLUGINS': {
        'basics': {
            'js': ['http://rawgithub.com/glenrobertson/leaflet-tilelayer-geojson/master/TileLayer.GeoJSON.js'],
            'auto-include': True
        },
        'markercluster': {
            'css': [
                '/static/css/MarkerCluster.Default.css',
                '/static/css/MarkerCluster.css'],
            'js': '/static/js/leaflet.markercluster.js',
            'auto-include': True,
        },
        'leaflet-ajax': {
            'js': '/static/js/leaflet.ajax.min.js',
            'auto-include': True,
        },
    }
}

SERIALIZATION_MODULES = {
    'geojson': 'djgeojson.serializers'
}

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    ),
    'PAGINATE_BY': 10
}

JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=14),
    'JWT_ALLOW_REFRESH': True,
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=14)
}

ALLOWED_HOSTS = []

CORS_ORIGIN_ALLOW_ALL = True

BROKER_URL = 'amqp://guest:guest@localhost:5672/'

# django-user-accounts
ACCOUNT_EMAIL_UNIQUE = False
ACCOUNT_EMAIL_CONFIRMATION_REQUIRED = True
ACCOUNT_USER_DISPLAY = lambda user: user.email

# password strength checking
PASSWORD_MIN_LENGTH = 8
PASSWORD_COMPLEXITY = {
    "LOWER": 1,
    "DIGITS": 1,
}

AUTH_USER_MODEL = 'sdauth.User'
AUTHENTICATION_BACKENDS = ('sdauth.backend.ModelBackend',)

RECORD_LOGIN = False

LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'
LOGIN_REDIRECT_URL = '/'

ACCOUNT_USE_AUTH_AUTHENTICATE = True


DEFAULT_THUMBNAIL_SIZE = (100, 100)

THUMBNAIL_ALIASES = {
    'sdauth.User.photo': {
        'small': {'size': DEFAULT_THUMBNAIL_SIZE, 'crop': True},
    },
}

# TODO move this to True on production
USE_ASYNC_IMPORT = False

# Caching configuration, you need redis installed in order to work, if not it will degrade graceful
CACHEOPS_REDIS = {
    'host': 'localhost',  # redis-server is on same machine
    'port': 6379,         # default redis port
    'db': 1,              # SELECT non-default redis database
    'socket_timeout': 3,  # using separate redis db or redis instance is highly recommended on production
}

CACHEOPS = {
    'censo.cliente': {'ops': 'all', 'timeout': 60*15},
}

CACHEOPS_DEFAULTS = {
    'timeout': 60*60
}

#CACHEOPS_DEGRADE_ON_FAILURE = True

# this provides a way of overwriting variables locally without
# adding it to git, use for TEST_CONCURRENCY, DATABASES
try:
    from localsettings import *
except ImportError:
    pass

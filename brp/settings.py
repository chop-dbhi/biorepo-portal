"""
Django settings for brp project.

Generated by 'django-admin startproject' using Django 1.9.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
import sys
import environ

from pythonjsonlogger import jsonlogger

root = environ.Path(__file__) - 2  # three folder back (/a/b/c/ - 3 = /)
env = environ.Env(DEBUG=(bool, False),)  # set default values and casting
environ.Env.read_env('{0}.env'.format(env('APP_ENV')))  # reading .env file

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_PORT = env.int('EMAIL_PORT')
EMAIL_SUBJECT_PREFIX = '[brp]'
FORCE_SCRIPT_NAME = env('FORCE_SCRIPT_NAME')
SECRET_KEY = env('SECRET_KEY')

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', [])

TIME_ZONE = env('TIME_ZONE', default='America/New_York')
DEBUG = env.bool('DEBUG')

# Application definition

INSTALLED_APPS = [
    'admin_tools',
    'admin_tools.theming',
    'admin_tools.menu',
    'admin_tools.dashboard',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.flatpages',
    'markdown_deux',
    'rest_framework.authtoken',
    'rest_framework',
    'registration',
    'session_security',
    'crispy_forms',
    'accounts',
    'brp',
    'api',
    'dataentry',
    'brp_admin',
    'social_django'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'brp.middleware.LoggingMiddleware',
    'brp.middleware.MaintenanceMiddleware',
    'session_security.middleware.SessionSecurityMiddleware',
    'dataentry.middleware.CheckPdsCredentialsMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'accounts.middleware.CheckEulaMiddleware',
]

ROOT_URLCONF = 'brp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        # 'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'libraries': {
                'formutils': 'brp.formutils'
            },
            'loaders': [
                'admin_tools.template_loaders.Loader',
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
        },
    },
]
ADMIN_TOOLS_MENU = 'brp_admin.menu.CustomMenu'

# TEMPLATE_LOADERS = (
#     'admin_tools.template_loaders.Loader',
# )

WSGI_APPLICATION = 'brp.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': env.db(),
}

CACHES = {
    'default': env.cache(),
}

AUTHENTICATION_BACKENDS = (
    # 'accounts.backends.LdapBackend',
    'django.contrib.auth.backends.ModelBackend',
    'accounts.auth0backend.Auth0'
)

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = []

# django auth user profile integration
AUTH_PROFILE_MODULE = 'accounts.UserProfile'

# django-registration
REGISTRATION_BACKENDS = {
    'default': 'accounts.backends.DefaultBackend',
}
REGISTRATION_ACTIVATION_DAYS = 0
REGISTRATION_MODERATION = True

ADMINS = (
    ('Alex Felmeister', 'felmeistera@email.chop.edu'),
    ('Alex Gonzalez', 'gonzalezak@email.chop.edu'),
    ('Edward Krause', 'krausee@email.chop.edu'),
    ('Suzanne Gerace', 'geraces@email.chop.edu'),
    ('EIG Support', 'eigsupport@email.chop.edu')
)
MANAGERS = ADMINS

ACCOUNT_MODERATORS = ADMINS

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'
LOGIN_REDIRECT_URL = '/'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

if DEBUG:
    STATIC_ROOT = str(root.path('_site/static/'))
else:
    STATIC_ROOT = '/opt/staticfiles/'
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Honest Broker Settings

SERVICE_CLIENT_SETTINGS = {
    "API_KEY": env('SERVICE_CLIENT_API_KEY'),
    "APP_URL": env('SERVICE_CLIENT_APP_URL'),
    "HOST": env('SERVICE_CLIENT_HOST'),
    "ISSECURE": env.bool('SERVICE_CLIENT_ISSECURE'),
    "ROOT_PATH": env('SERVICE_CLIENT_ROOT_PATH'),
    "SELF_ROOT_PATH": env('SERVICE_CLIENT_SELF_ROOT_PATH')
}

PROTOCOL_PROPS = {
    "CLIENT_KEY": {
        "key": env('PROTOCOL_PROPS_CLIENT_KEY')
    },
    "IMMUTABLE_KEYS": {
        "length": env.int('IMMUTABLE_KEY_LENGTH'),
        "seed": env.int('IMMUTABLE_KEY_SEED')
    }
}

SITE_ID = 1

PLUGINS = {}

SESSION_SECURITY_WARN_AFTER = 900
SESSION_SECURITY_EXPIRE_AFTER = 1200
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

DEFAULT_FROM_EMAIL = 'eigsupport@email.chop.edu'

# Django Rest Framework
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    ),
    'FORM_METHOD_OVERRIDE': None,
    'FORM_CONTENT_OVERRIDE': None,
    'FORM_CONTENTTYPE_OVERRIDE': None
}

# LDAP integration
LDAP = {}
LDAP['DEBUG'] = env.bool('LDAP_DEBUG')
LDAP['PREBINDDN'] = env.str('LDAP_PREBINDDN')
LDAP['SEARCHDN'] = env.str('LDAP_SEARCHDN')
LDAP['SEARCH_FILTER'] = env.str('LDAP_SEARCH_FILTER')
LDAP['SERVER_URI'] = env('LDAP_SERVER_URI')
LDAP['PREBINDPW'] = env('LDAP_PREBINDPW')
LDAP['MAX_AGE'] = env.int('LDAP_MAX_AGE')

# Enable Performance logging of 'ehb-client' logging facility
EHB_LOG = env.bool('EHB_LOG', True)

# Logging Facilities
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
        'json': {
            '()': jsonlogger.JsonFormatter,
            'fmt': '%(levelname)s %(asctime)s %(module)s %(process)d%(message)s %(pathname)s $(lineno)d $(funcName)s',

        }
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'default': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
            'formatter': 'json',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        }
    },
    'loggers': {
        '': {
            'handlers': ['default'],
            'level': 'DEBUG',
            'propagate': False
        },
        'django.request': {
            'handlers': ['default'],
            'level': 'DEBUG',
            'propagate': False
        },
        'brp.middleware': {
            'handlers': ['default'],
            'propagate': False,
        },
        'api.views': {
            'handlers': ['default'],
            'propagate': False,
        },
        'accounts.backends': {
            'handlers': ['default'],
            'propagate': False,
        },
        'ehb-client': {
            'level': 'DEBUG',
            'handlers': ['default'],
            'propagate': False,
        }
    }
}

if FORCE_SCRIPT_NAME:
    ADMIN_MEDIA_PREFIX = os.path.join(
        FORCE_SCRIPT_NAME, ADMIN_MEDIA_PREFIX[1:])
    STATIC_URL = os.path.join(FORCE_SCRIPT_NAME, STATIC_URL[1:])
    LOGIN_URL = os.path.join(FORCE_SCRIPT_NAME, LOGIN_URL[1:])
    LOGOUT_URL = os.path.join(FORCE_SCRIPT_NAME, LOGOUT_URL[1:])
    LOGIN_REDIRECT_URL = os.path.join(
        FORCE_SCRIPT_NAME, LOGIN_REDIRECT_URL[1:])

##### Auth 0 settings #####
SOCIAL_AUTH_TRAILING_SLASH = False  # Remove trailing slash from routes
SOCIAL_AUTH_AUTH0_DOMAIN = env('AUTH0_CLIENT_ID')
SOCIAL_AUTH_AUTH0_KEY = env('AUTH0_CLIENT_ID')
SOCIAL_AUTH_AUTH0_SECRET = env('AUTH0_CLIENT_SECRET')
SOCIAL_AUTH_AUTH0_SCOPE = [
    'openid',
    'profile',
    'email'
]
SOCIAL_AUTH_AUTH0_DOMAIN = env('AUTH0_DOMAIN')
if env('AUTH0_AUDIENCE'):
    AUDIENCE = env('AUTH0_AUDIENCE')
else:
    if SOCIAL_AUTH_AUTH0_DOMAIN:
        AUDIENCE = 'https://' + SOCIAL_AUTH_AUTH0_DOMAIN + '/userinfo'
if AUDIENCE:
    SOCIAL_AUTH_AUTH0_AUTH_EXTRA_ARGUMENTS = {'audience': AUDIENCE}
AUTHENTICATION_BACKENDS = {
    'auth0login.auth0backend.Auth0',
    'django.contrib.auth.backends.ModelBackend'
}


# LOGIN_URL = '/login/auth0'
# LOGIN_REDIRECT_URL = '/dashboard'

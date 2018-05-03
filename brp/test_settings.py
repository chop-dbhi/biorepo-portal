"""
Django test settings for brp project.
"""
import os
import environ
root = environ.Path(__file__) - 2  # three folder back (/a/b/c/ - 3 = /)
env = environ.Env(DEBUG=(bool, False),)  # set default values and casting

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/
EMAIL_HOST = 'localhost'
EMAIL_PORT = 25
EMAIL_SUBJECT_PREFIX = '[brp]'
FORCE_SCRIPT_NAME = ''
SECRET_KEY = 'secretkey'


TIME_ZONE = env('TIME_ZONE', default='America/New_York')
DEBUG = env.bool('DEBUG')

# Application definition

INSTALLED_APPS = [
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
    'accounts',
    'brp',
    'brp_admin',
    'api',
    'dataentry',
]

MIDDLEWARE_CLASSES = [
    'brp.middleware.LoggingMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
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
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'libraries': {
                'formutils': 'brp.formutils'
            }
        },
    },
]

WSGI_APPLICATION = 'brp.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': env.db('SQLITE_URL', default='sqlite:///test.db'),
}

AUTHENTICATION_BACKENDS = (
    'accounts.backends.LdapBackend',
    'django.contrib.auth.backends.ModelBackend',
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
    ('Tyler Rivera', 'riverat2@email.chop.edu'),
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

STATIC_ROOT = str(root.path('_site/static/'))
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Honest Broker Settings

SERVICE_CLIENT_SETTINGS = {
    "API_KEY": 'testkey',
    "APP_URL": 'http://example.com',
    "HOST": 'example.com',
    "ISSECURE": False,
    "ROOT_PATH": '',
    "SELF_ROOT_PATH": ''
}

PROTOCOL_PROPS = {
    "CLIENT_KEY": {
        "key": 'testclientkey'
    },
    "IMMUTABLE_KEYS": {
        "length": 10,
        "seed": 123456789
    }
}

SITE_ID = 1

PLUGINS = {}

SESSION_SECURITY_WARN_AFTER = 900
SESSION_SECURITY_EXPIRE_AFTER = 1200
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

DEFAULT_FROM_EMAIL = 'test@example.com'

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
}

# LDAP integration
LDAP = {}
LDAP['DEBUG'] = ''
LDAP['PREBINDDN'] = 'prebinddn'
LDAP['SEARCHDN'] = 'searchdn'
LDAP['SEARCH_FILTER'] = '(sAMAccountName={0})'
LDAP['SERVER_URI'] = 'example.com'
LDAP['PREBINDPW'] = 'ldappassword'
LDAP['MAX_AGE'] = 180

if FORCE_SCRIPT_NAME:
    ADMIN_MEDIA_PREFIX = os.path.join(
        FORCE_SCRIPT_NAME, ADMIN_MEDIA_PREFIX[1:])
    STATIC_URL = os.path.join(FORCE_SCRIPT_NAME, STATIC_URL[1:])
    LOGIN_URL = os.path.join(FORCE_SCRIPT_NAME, LOGIN_URL[1:])
    LOGOUT_URL = os.path.join(FORCE_SCRIPT_NAME, LOGOUT_URL[1:])
    LOGIN_REDIRECT_URL = os.path.join(
        FORCE_SCRIPT_NAME, LOGIN_REDIRECT_URL[1:])

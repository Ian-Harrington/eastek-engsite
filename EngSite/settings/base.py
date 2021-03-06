"""
Django settings for EngSite project.

Generated by 'django-admin startproject' using Django 1.11.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
from django.utils.translation import ugettext_lazy as _

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

#================================
#=        CORE SETTINGS         =
#================================
# SECURITY WARNING: keep the secret key used in production secret!
# MUST DEFINE THE SECRET_KEY IN EACH OF THE EXTENDED SETTINGS
SECRET_KEY = None  

# SECURITY WARNING: don't run with debug turned on in production!
# Set explicitly in extended settings
DEBUG = False
ADMINS = [('Ian Harrington', 'ian.harrington@eastekinternational.com')]
MANAGERS = ADMINS

# Set explicitly in extended settings
ALLOWED_HOSTS = ['*']

# Where to find site URLs
ROOT_URLCONF = 'EngSite.urls'

# Application definition
WSGI_APPLICATION = 'EngSite.wsgi.application'

# Set this to prevent bots from visiting the site
#   List of compiled regex objects
DISALLOWED_USER_AGENTS = []

# Server Timezone
TIME_ZONE = 'Asia/Shanghai'
# Make Django timezone aware (only useful for LZ)
USE_TZ = True


# Installation language
LANGUAGE_CODE = 'en-us'


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

# Whether to use internationalization or not
USE_I18N = True

# Supported languages
LANGUAGES = [
    ('en', _('English')),
    ('zh-hans', _('Chinese')),
]

LANGUAGE_COOKIE_NAME = 'language'

# Where translations are stored
LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'EngSite/translations')
]


# Whether to use Localizated date formats or not
USE_L10N = False

# Date/Time display formats
SHORT_DATE_FORMAT = DATE_FORMAT = 'Y-n-j' # 2006-10-25
SHORT_DATETIME_FORMAT = DATETIME_FORMAT = 'Y-n-j | G:i' # 2006-10-25 | 14:30
TIME_FORMAT = 'G:i' # 14:30
# Date[Time] input formats (uses python string parsing)
DATE_INPUT_FORMATS = [
    '%Y-%m-%d', '%Y/%m/%d', '%Y.%m.%d',  # '2006-10-25', '2006/10/25', '2006.10.25'
    '%m/%d/%Y', '%m-%d-%Y',              # '10/25/2006', '10-25-2006'
    '%b %d %Y', '%d %b %Y',              # 'Oct 25 2006', '25 Oct 2006'
]
DATETIME_INPUT_FORMATS = [
    '%Y-%m-%d %H:%M:%S',     # '2006-10-25 14:30:59'
    '%Y-%m-%d %H:%M:%S.%f',  # '2006-10-25 14:30:59.000200'
    '%Y-%m-%d %H:%M',        # '2006-10-25 14:30'
    '%Y-%m-%d',              # '2006-10-25'
    '%Y/%m/%d %H:%M:%S',     # '2006/10/25 14:30:59'
    '%Y/%m/%d %H:%M:%S.%f',  # '2006/10/25 14:30:59.000200'
    '%Y/%m/%d %H:%M',        # '2006/10/25 14:30'
    '%Y/%m/%d',              # '2006/10/25'
    '%Y.%m.%d %H:%M:%S',     # '2006.10.25 14:30:59'
    '%Y.%m.%d %H:%M:%S.%f',  # '2006.10.25 14:30:59.000200'
    '%Y.%m.%d %H:%M',        # '2006.10.25 14:30'
    '%Y.%m.%d',              # '2006.10.25'
    '%m/%d/%Y %H:%M:%S',     # '10/25/2006 14:30:59'
    '%m/%d/%Y %H:%M:%S.%f',  # '10/25/2006 14:30:59.000200'
    '%m/%d/%Y %H:%M',        # '10/25/2006 14:30'
    '%m/%d/%Y',              # '10/25/2006'
    '%m/%d/%y %H:%M:%S',     # '10/25/06 14:30:59'
    '%m/%d/%y %H:%M:%S.%f',  # '10/25/06 14:30:59.000200'
    '%m/%d/%y %H:%M',        # '10/25/06 14:30'
    '%m/%d/%y',              # '10/25/06'
]

# Registered Applications (can access all functionality)
INSTALLED_APPS = [
    'projects.apps.ProjectsConfig',
    'overtime.apps.OvertimeConfig',
    'users.apps.UsersConfig',
    'employees.apps.EmployeesConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

#DB = open(os.path.join(BASE_DIR, 'EngSite/DB_account.txt'))
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'projecteng',
        # Set explicitly in extended settings
        'USER': '',
        'PASSWORD': '',
        'HOST': '', # only use if db is on different server
        'PORT': '', # only use if HOST != ''
    }
}

# Where to find and how to process HTML templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'EngSite/templates')],
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



#================================
#=          MIDDLEWARE          =
#================================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


#================================
#=        AUTHENTICATION        =
#================================

AUTH_USER_MODEL = 'users.User'

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    #{'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# The login page
LOGIN_URL = '/login/'
# Page to view after login if none specified
LOGIN_REDIRECT_URL = '/'


#================================
#=         STATICFILES          =
#================================

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'EngSite/static/'),
]

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
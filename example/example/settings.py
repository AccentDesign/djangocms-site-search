import os
import sys

from django.utils.translation import ugettext_lazy as _


BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Security
# WARNING: keep the secret key used in production secret!
SECRET_KEY = 'SOME SECRET KEY THAT NEEDS CHANGING'

DEBUG = True

ALLOWED_HOSTS = ['*']

INTERNAL_IPS = ('127.0.0.1', )


# Application definition
SITE_ID = 1

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/admin/login/'

INSTALLED_APPS = (
    'djangocms_admin_style',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # CMS
    'bootstrap3',
    'djangocms_text_ckeditor',
    'cms',
    'treebeard',
    'menus',
    'sekizai',
    'djangocms_file',
    'djangocms_inherit',
    'djangocms_link',
    'djangocms_picture',
    'djangocms_snippet',
    'djangocms_teaser',

    # Search
    'site_search',

)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
    'cms.middleware.language.LanguageCookieMiddleware',
)

ROOT_URLCONF = 'example.urls'

WSGI_APPLICATION = 'example.wsgi.application'


# Search
PLACEHOLDERS_SEARCH_LIST = {
    '*': {},
}


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

MIGRATION_MODULES = {
    'djangocms_file': 'djangocms_file.migrations_django',
    'djangocms_inherit': 'djangocms_inherit.migrations_django',
    'djangocms_picture': 'djangocms_picture.migrations_django',
    'djangocms_snippet': 'djangocms_snippet.migrations_django',
    'djangocms_teaser': 'djangocms_teaser.migrations_django',
}


# Internationalization
LANGUAGE_CODE = 'en'

LANGUAGES = (
    ('en', _('English')),
)

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'collected_static')

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), '/media')
MEDIA_URL = '/media/'


# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.core.context_processors.i18n',
                'django.core.context_processors.request',
                'django.core.context_processors.media',
                'django.core.context_processors.static',
                'sekizai.context_processors.sekizai',
                'cms.context_processors.cms_settings',
            ],
        },
    },
]


# CMS
CMS_PERMISSION = True
CMS_TEMPLATES = (
    ('cms/layouts/fullwidth.html',
     _('Full Width')),
)


# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'detail': {
            'format': (
                '%(levelname)s %(asctime)s %(pathname)s:%(lineno)s '
                '[%(funcName)s] %(message)s')
        }
    },
    'handlers': {
        'stdout': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'detail',
            'stream': sys.stdout
        }
    },
    'loggers': {
        'django': {
            'handlers': ['stdout'],
            'level': 'INFO',
        },
        '': {
            'handlers': ['stdout'],
            'level': 'INFO',
        }
    }
}

import os
import sys

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
# ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'

def rel(*x):
    return os.path.normpath(
        os.path.join(os.path.abspath(os.path.dirname(__file__)), *x),
    )
PROJECT_ROOT = rel('..')
root = lambda *x: os.path.abspath(
    os.path.join(os.path.abspath(PROJECT_ROOT), *x))
etc_dir = lambda *x: os.path.abspath(os.path.join(root('etc'), *x))

sys.path.append(root('apps'))

_ = lambda s: s

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': root('..', 'dev.db'),
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',
        'PORT': '',
    }
}

TIME_ZONE = 'Europe/Kiev'

LANGUAGE_CODE = 'ru'

SITE_ID = 1

USE_I18N = True
USE_L10N = True

MEDIA_ROOT = root('media')
MEDIA_URL = '/media/'
STATIC_ROOT = root('static')
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    root('static/common'),
)


STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #'django.contrib.staticfiles.finders.DefaultStorageFinder',
    )

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #'django.template.loaders.eggs.Loader',
    )

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    )


MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    )

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    root('templates'),
    )

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',

    'timing',

    'jsonrpc',
    'south',
    )

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
            },
        }
}

try:
    from local import *
except:
    print 'please add local.py'


"""
Django settings for hydroponics project.
"""
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LOG_DIR = os.path.join(BASE_DIR, 'logs')

STATIC_URL = '/static/'
STATIC_DIR = os.path.join(BASE_DIR, 'logs')
STATIC_ROOT = BASE_DIR + STATIC_URL

ALLOWED_HOSTS = ["192.168.0.28", "169.254.248.180"]

ADMINS = [('Preston Sheppard', 'psheppard16@gmail.com')]
DEBUG = True

INSTALLED_APPS = (
	'admin_view_permission',
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'rest_framework',
	'nested_inline',
	'import_export',
    'hydro.apps.HydroConfig',
)

MIDDLEWARE = (
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

REST_FRAMEWORK = {
	# Use Django's standard `django.contrib.auth` permissions, or allow read-only access for unauthenticated users.
	'DEFAULT_PERMISSION_CLASSES': [
		'rest_framework.permissions.DjangoModelPermissions',
		'rest_framework.permissions.IsAuthenticated',
	]
}

REST_FRAMEWORK_EXTENSIONS = {
	'DEFAULT_USE_CACHE': 'default',
	'DEFAULT_CACHE_RESPONSE_TIMEOUT': 60 * 15
}

CACHES = {
	'default': {
		'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
		'LOCATION': '127.0.0.1:11211',
	}
}

ROOT_URLCONF = 'hydroponics.urls'

TEMPLATE_DEBUG = None

TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [os.path.join(BASE_DIR, 'templates')],
		'APP_DIRS': True,
		'OPTIONS': {
			'debug': None,
			'context_processors': [
				'django.template.context_processors.debug',
				'django.template.context_processors.request',
				'django.contrib.auth.context_processors.auth',
				'django.contrib.messages.context_processors.messages',
				'django.template.context_processors.media',
				'django.template.context_processors.static',
			],
			'libraries': {
			}
		},
	},
]


WSGI_APPLICATION = 'hydroponics.wsgi.application'

USE_TZ = True
TIME_ZONE = 'America/New_York'

USE_I18N = True
USE_L10N = True

LANGUAGE_CODE = 'en-us'

LOGGING = {
	'version': 1,
	'disable_existing_loggers': True,
	'formatters': {
		'standard': {
			'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
			'datefmt': "%d/%b/%Y %H:%M:%S"
		},
	},
	'handlers': {
		'null': {
			'level': 'DEBUG',
			'class': 'logging.NullHandler',
		},
		'hydrologfile': {
			'level': 'DEBUG',
			'class': 'logging.handlers.RotatingFileHandler',
			'filename': os.path.join(LOG_DIR, 'hydro.log'),
			'maxBytes': 50000,
			'backupCount': 2,
			'formatter': 'standard',
		},
		'dblogfile': {
			'level': 'INFO',
			'class': 'logging.handlers.RotatingFileHandler',
			'filename': os.path.join(LOG_DIR, 'db_sql.log'),
			'maxBytes': 50000,
			'backupCount': 2,
			'formatter': 'standard',
		},
		'console': {
			'level': 'DEBUG',
			'class': 'logging.StreamHandler',
			'formatter': 'standard'
		},
	},
	'loggers': {
		'django': {
			'handlers': ['console'],
			'propagate': True,
			'level': 'WARN',
		},
		'django.db.backends': {
			'handlers': ['dblogfile'],
			'level': 'DEBUG',
			'propagate': False,
		},
		'hydro': {
			'handlers': ['console', 'hydrologfile'],
			'level': 'DEBUG',
		}
	}
}

from hydroponics.settings_secret import *

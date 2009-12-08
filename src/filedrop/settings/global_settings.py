# Global Settings for FileDrop
import os
import filedrop

# FileDrop Settings
FILEDROP_ROOT = os.path.normpath(os.path.join(filedrop.__path__), "../../"))
USE_XSENDFILE = False

# Database Settings
DATABASE_ENGINE = ''           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = ''             # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Cache Settings
CACHE_MIDDLEWARE_SECONDS = 60 * 15
CACHE_MIDDLEWARE_KEY_PREFIX = "filedrop"
CACHE_MIDDLEWARE_ANONYMOUS_ONLY = True

# Local Install Settings
DEBUG = False
TEMPLATE_DEBUG = DEBUG
TIME_ZONE = 'America/Los_Angeles'
SITE_ID = 1
USE_ETAGS = True
USE_I18N = False
LANGUAGE_CODE = 'en-us'
MANAGERS = ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)


# Email Settings
EMAIL_SUBJECT_PREFIX = '[FileDrop] '
DEFAULT_FROM_EMAIL = SERVER_EMAIL = 'webmaster@example.com'

# Media Settings
MEDIA_ROOT = ''
MEDIA_URL = ''
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = ''

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'django.middleware.http.ConditionalGetMiddleware',
    # 'django.middleware.gzip.GZipMiddleware',
    'django.middleware.common.CommonMiddleware',
)

ROOT_URLCONF = 'filedrop.urls'

TEMPLATE_DIRS = (
    os.path.normpath(os.path.join(filedrop.__path__), "templates"))
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'filedrop'
)

# Development Settings
from filedrop.settings.global_settings import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

MANAGERS = ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = os.path.normpath(os.path.join(FILEDROP_ROOT, "devel.db"))
CACHE_BACKEND = 'locmem:///'

MEDIA_ROOT = os.path.normpath(os.path.join(FILEDROP_ROOT, "public"))
MEDIA_URL = 'http://127.0.0.1:8000/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = ''

# Extra development only apps?
# INSTALLED_APPS += 
MIDDLEWARE_CLASSES = MIDDLEWARE_CLASSES + ('djangologging.middleware.LoggingMiddleware',)

# Django Logging!
LOGGING_OUTPUT_ENABLED = True
LOGGING_INTERCEPT_REDIRECTS = True
LOGGING_LOG_SQL = True
INTERNAL_IPS = ('127.0.0.1')

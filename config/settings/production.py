from .base import *
import dj_database_url

DEBUG = False

db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

INSTALLED_APPS += (
    'raven.contrib.django.raven_compat',
)


ALLOWED_HOSTS += (
    '.herokuapp.com',
    'platform.theprate.com',
)

# CORS_ORIGIN_ALLOW_ALL = True

CORS_ORIGIN_WHITELIST = (
    'www.theprate.com',
    'theprate.com',
    'thedrab.co',
    'www.thedrab.co',
    'localhost:3474',
    'localhost:3000',
    'localhost:8080',
    'localhost',
    'theprate-staging.herokuapp.com',
    'jetpath.surge.sh',
    'theprate.herokuapp.com',
)


STATIC_ROOT = os.path.join(ROOT_DIR, 'staticfiles')
MEDIA_ROOT = os.path.join(ROOT_DIR, 'mediafiles')
STATIC_URL = '/static/'


STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

RAVEN_CONFIG = {
    'dsn': 'https://ab65a1f98f1541c884de75dc63332cbb:81462565e6bc4421bfd36c07cfe105e1@app.getsentry.com/89717',
    # If you are using git, you can also automatically configure the
    # release based on the git info.
    'release': os.getenv('HEROKU_SLUG_COMMIT', 'unknown'),
}

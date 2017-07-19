import os

from .base import *


DEBUG = False

INSTALLED_APPS += (
    'raven.contrib.django.raven_compat',
    'gunicorn',
)


ALLOWED_HOSTS += (
    '.herokuapp.com',
    'platform.theprate.com',
    'platform.thedrab.com',
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
    'jetpath.theprate.com',
    'theprate.herokuapp.com',
)

SECURE_HSTS_SECONDS = 60
SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool(
    'DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS', default=True)
SECURE_CONTENT_TYPE_NOSNIFF = env.bool(
    'DJANGO_SECURE_CONTENT_TYPE_NOSNIFF', default=True)
SECURE_BROWSER_XSS_FILTER = True
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SECURE_SSL_REDIRECT = env.bool('DJANGO_SECURE_SSL_REDIRECT', default=True)
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
X_FRAME_OPTIONS = 'DENY'

SECRET_KEY = env('DJANGO_SECRET_KEY')


STATIC_URL = 'static/'


STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'


RAVEN_CONFIG = {
    'dsn': 'https://ab65a1f98f1541c884de75dc63332cbb:81462565e6bc4421bfd36c07cfe105e1@app.getsentry.com/89717',
    # If you are using git, you can also automatically configure the
    # release based on the git info.
    'release': os.getenv('HEROKU_SLUG_COMMIT', 'unknown'),
}

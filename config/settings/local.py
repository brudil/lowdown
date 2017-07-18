from .base import *

DEBUG = env.bool('DJANGO_DEBUG', default=True)
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

SECRET_KEY = env('DJANGO_SECRET_KEY', default='JoSFa+zip%}rS?L3K~:,Y6jP$}~qBXFBShQ>ALf`q!fD{&m8-E')

INSTALLED_APPS += (
    'django_extensions',
)

REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] += (
    'rest_framework.renderers.BrowsableAPIRenderer',
)

ALLOWED_HOSTS = ('.ngrok.io', 'localhost', )

MIDDLEWARE += (
    #'querycount.middleware.QueryCountMiddleware',
)

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

JWT_AUTH['JWT_VERIFY_EXPIRATION'] = False

CORS_ORIGIN_ALLOW_ALL = True

LOGGING = {
    'disable_existing_loggers': False,
    'version': 1,
    'handlers': {
        'console': {
            # logging handler that outputs log messages to terminal
            'class': 'logging.StreamHandler',
            'level': 'DEBUG', # message level to be written to console
        },
    },
    'loggers': {
        '': {
            # this sets root level logger to log debug and higher level
            # logs to console. All other loggers inherit settings from
            # root level logger.
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False, # this tells logger to send logging message
            # to its parent (will send if set to True)
        },
        'django.db': {
            'level': 'DEBUG',
        },
    },
}

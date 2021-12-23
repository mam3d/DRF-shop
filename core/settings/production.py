from .base import *
DEBUG = False
ALLOWED_HOSTS = ["localhost"]
INSTALLED_APPS += ["whitenoise.runserver_nostatic"]
MIDDLEWARE += ['whitenoise.middleware.WhiteNoiseMiddleware']
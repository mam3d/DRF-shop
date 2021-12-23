from decouple import config
from core.celery import app

__all__ = ["app"]

if config("PRODUCTION", default=0, cast=int) == 1:
    from .production import *
else:
    from .local import *
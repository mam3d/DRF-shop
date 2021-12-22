from decouple import config

if config("PRODUCTION", default=0, cast=int) == 1:
    from .production import *
else:
    from .local import *
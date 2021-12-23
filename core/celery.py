import os
from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE","core.settings")

app = Celery()
app.config_from_object("core.settings:base")
app.autodiscover_tasks()


if __name__ == "__main__":
    app.start()
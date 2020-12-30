import os

from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULES", "core.settings")
app = Celery("core")
app.config_from_object("django.conf.settings", namespace="CELERY")
app.autodiscover_tasks()

# DJANGO_SETTINGS_MODULE is for celery to know hot to find the Django project
# celery instance with the name "core" is created and is assigned to variable called "app"
# config_from_object loads celery configuration files from the settings object. Namespace "CELERY" exists to prevent clashes with other Django settings. All config settings will be prefixed with CELERY_
# autodiscover tasks means Django will automatically look for tasks in applications mentioned in settings.INSTALLED_APPS

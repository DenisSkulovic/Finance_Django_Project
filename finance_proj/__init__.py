from .celery import app as celery_app

__all__ = ("celery_app", )

#  this code ensures celery is automatically imported at Django start
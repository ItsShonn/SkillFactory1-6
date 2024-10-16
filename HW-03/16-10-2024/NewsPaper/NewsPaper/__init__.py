from .celery import app as celery_app

__all__ = ('celery_app',)
CELERY_IMPORTS = ('news.tasks')
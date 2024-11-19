from __future__ import absolute_import, unicode_literals

# This ensures the app is always imported when
# Django starts
from .celery import app as smartroll_celery

__all__ = ('smartroll_celery',)

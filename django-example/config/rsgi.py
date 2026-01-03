"""
RSGI config for demo project.

It exposes the RSGI callable as a module-level variable named ``application``.
"""

import os

from django_rsgi import get_rsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

application = get_rsgi_application()

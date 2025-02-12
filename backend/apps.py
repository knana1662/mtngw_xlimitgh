from django.apps import AppConfig
from pathlib import Path
from sys import path

from core import BACKEND_ROOT_PATH


class BackendConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'backend'
    path = BACKEND_ROOT_PATH

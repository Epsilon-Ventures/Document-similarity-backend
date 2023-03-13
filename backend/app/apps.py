from django.apps import AppConfig
from .models import load_model

class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'

    def ready(self):
        """Loads the model when the app is ready"""
        load_model()

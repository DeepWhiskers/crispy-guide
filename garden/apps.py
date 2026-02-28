from django.apps import AppConfig


class GardenConfig(AppConfig):
    """Asetukset garden-sovellukselle."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'garden'
    verbose_name = 'Puutarhapäiväkirja'

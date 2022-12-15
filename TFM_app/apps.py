from django.apps import AppConfig


class TfmAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'TFM_app'


class PredictConfig(AppConfig):
    name = 'predict'
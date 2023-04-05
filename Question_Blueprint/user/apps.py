from django.apps import AppConfig


class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user'


#  get signal to create a profile
    def ready(self):
        import user.signals
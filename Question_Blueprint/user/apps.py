from django.apps import AppConfig

# AppConfig for the User app

class UserConfig(AppConfig):
    # Default auto field for the app
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user'

    # Importing signals module to create a profile when a new user is created
    def ready(self):
        import user.signals

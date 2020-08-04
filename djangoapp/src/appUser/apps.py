from django.apps import AppConfig


class AppuserConfig(AppConfig):
    name = 'appUser'

    def ready(self):
        """ Related to signals """        
        import appuser.signals
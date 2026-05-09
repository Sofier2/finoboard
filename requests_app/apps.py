from django.apps import AppConfig
import os


class RequestsAppConfig(AppConfig):

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'requests_app'

    def ready(self):

        if os.environ.get('RUN_MAIN') != 'true':
            return

        print(">>> READY CALLED")

        from citizen_system.arduino_bridge import start_arduino_thread
        start_arduino_thread()
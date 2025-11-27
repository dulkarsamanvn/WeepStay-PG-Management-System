from django.core.management.base import BaseCommand,CommandError
from django.conf import settings
from django.core.management import call_command
from core.settings import CUSTOM_APPS
from core_utils.utils.db_utils.get_custom_apps import GetCustomApps

class Command(BaseCommand,GetCustomApps):
    help = "Custom makemigrations command for only CUSTOM_APPS defined in settings.py"

    CUSTOM_APPS = getattr(settings,"CUSTOM_APPS")

    def handle(self, *args, **options):
        custom_apps = self.refactor_command(CUSTOM_APPS)

        if not custom_apps:
            raise CommandError("CUSTOM_APPS is not defined in settings.py file")
        
        try:
            call_command("makemigrations",*custom_apps)
            self.stdout.write(f"Migrations created for apps: {custom_apps}")
        except Exception as e:
            self.stderr.write(f"Error creating migrations for {custom_apps}: {e}")
        
from django.core.management.base import BaseCommand
import os,shutil

class Command(BaseCommand):
    help : str = "Deletes all migration folders and their contents from all Django apps"

    def handle(self,*args,**kwargs):
        project_root = os.getcwd()

        for root,dirs,files in os.walk(project_root):
            if "migrations" in dirs:
                migrations_dirs = os.path.join(root,"migrations")
                self.stdout.write(f"Deleting migrations folder: {migrations_dirs}")
                try:
                    shutil.rmtree(migrations_dirs)
                    self.stdout.write(
                        f"Successfully removed directory : {migrations_dirs}"
                    )
                
                except Exception as e:
                    self.stderr.write(f"Error removing directory {migrations_dirs}: {e}")
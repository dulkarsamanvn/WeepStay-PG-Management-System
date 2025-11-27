from django.core.management.base import BaseCommand
import os,shutil

class Command(BaseCommand):
    help : str = "Playground Shell"

    def handle(self,*args,**kwargs):
        pass
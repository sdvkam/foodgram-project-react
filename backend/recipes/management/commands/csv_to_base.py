import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand
from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Move data from .csv files to database'

    def handle(self, *args, **options):
        dir_files = os.path.join(settings.BASE_DIR, 'data')
        file_name = 'ingredients.csv'
        file_name = os.path.join(dir_files, file_name)
        one_file = open(file_name)
        reader = csv.reader(one_file, delimiter=',')
        for row in reader:
            Ingredient.objects.create(
                name=row[0],
                measurement_unit=row[1],
            )
        one_file.close()

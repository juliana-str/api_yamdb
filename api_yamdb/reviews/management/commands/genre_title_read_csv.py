import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand
from reviews.models import Genre_title


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open(
                os.path.join(
                    settings.BASE_DIR,
                    'static', 'data', 'genre_title.csv',
                ),
                'r', encoding='utf-8'
        ) as f:
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                if row[0] == 'id':
                    continue
                Genre_title.objects.get_or_create(
                    id=row[0],
                    title_id=row[1],
                    genre_id=row[2],
                )

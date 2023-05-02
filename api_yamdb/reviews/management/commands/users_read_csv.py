import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand
from reviews.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open(
            os.path.join(
                settings.BASE_DIR,
                'static', 'data', 'users.csv',
            ),
            'r', encoding='utf-8'
        ) as f:
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                if not isinstance(row[0], int):
                    continue
                User.objects.get_or_create(
                    id=row[0],
                    username=row[1],
                    email=row[2],
                    role=row[3],
                    bio=row[4],
                    first_name=row[5],
                    last_name=row[6]
                )

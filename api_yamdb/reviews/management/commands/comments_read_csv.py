import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from reviews.models import Comment


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open(
            os.path.join(
                settings.BASE_DIR,
                'static', 'data', 'comments.csv',
                    ),
            'r', encoding='utf-8'
                   ) as f:
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                if row[0] == 'id':
                    continue
                Comment.objects.get_or_create(
                    id=row[0],
                    review_id=row[1],
                    text=row[2],
                    author_id=row[3],
                    pub_date=row[4]
                )

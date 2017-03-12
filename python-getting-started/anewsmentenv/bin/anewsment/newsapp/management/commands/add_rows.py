from myapp.models import Forum, Jornada, ProPublica
from postgres_copy import CopyMapping
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        c = CopyMapping(
            # Give it the model
            Forum,
            # The path to your CSV
            args[1],
            # And a dict mapping the  model fields to CSV headers
            dict(article_title='article_title')
        )
        # Then save it.
        c.save()
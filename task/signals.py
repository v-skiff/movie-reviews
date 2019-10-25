import os
from threading import Thread

from django.db.models.signals import post_save
from django.conf import settings

from .models import Task

from catalog.management.commands.get_movies import run_crawler


def handler_run_scraper(sender, instance, **kwargs):
    if kwargs.get('created'):
        if instance.task == 'run_scraper':
            Thread(target=run_crawler, args=(instance,)).start()
        elif instance.task == 'count_images':
            count_images = os.listdir(
                os.path.join(settings.BASE_DIR, 'media/books_images'))
            instance.status = f'images: {len(count_images)}'
            instance.save()


post_save.connect(handler_run_scraper, sender=Task)

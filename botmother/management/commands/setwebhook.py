from django.conf import settings
from django.core.management.base import BaseCommand
import urllib.request


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('url', type=str, help='Backend domain')

    def handle(self, *args, **kwargs):
        bot_url = f'https://api.telegram.org/bot{settings.BOT_TOKEN}'
        webhook = kwargs["url"].strip("https://").strip("/")
        urllib.request.urlopen(f'{bot_url}/deleteWebhook')
        urllib.request.urlopen(f'{bot_url}/setWebhook?url=https://{webhook}')

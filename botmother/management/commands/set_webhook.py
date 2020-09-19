import requests
from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('domain', type=str, help='Backend domain')

    def handle(self, *args, **kwargs):
        bot_url = f'https://api.telegram.org/bot{settings.BOT_TOKEN}'
        webhook = kwargs["domain"].strip("https://").strip("/")
        requests.get(f'{bot_url}/deleteWebhook')
        requests.get(f'{bot_url}/setWebhook?url=https://{webhook}/botmother')

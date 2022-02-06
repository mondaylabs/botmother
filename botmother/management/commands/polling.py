import json
import time
from django.conf import settings
from django.core.management.base import BaseCommand

from botmother.utils.api import TelegramAPI
from botmother.utils.bot_router import BotRouter
from example.urls import dispatch


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        telegram = TelegramAPI(settings.BOT_TOKEN)
        updates_id = []

        while True:
            updates = telegram.get_updates()

            for update in updates['result']:
                if len(updates_id) == 0:
                    updates_id.append(update['update_id'])

                if update['update_id'] not in updates_id:
                    updates_id.append(update['update_id'])
                    router = BotRouter(json.dumps(update))
                    dispatch(router)

            time.sleep(settings.BOT_POOLING_INTERVAL or 5)

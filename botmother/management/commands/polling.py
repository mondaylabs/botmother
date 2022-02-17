import json
import time
import importlib

from django.conf import settings
from django.core.management.base import BaseCommand
from botmother.utils.api import TelegramAPI
from botmother.utils.bot_router import BotRouter


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        module_name, func_name = settings.BOT_POOLING_DISPATCHER.rsplit('.', 1)
        module = importlib.import_module(module_name)
        dispatch = getattr(module, func_name)
        telegram = TelegramAPI(settings.BOT_TOKEN)
        last_update = 0 or -1

        try:
            while True:
                time.sleep(settings.BOT_POOLING_INTERVAL or 3)
                updates = telegram.get_updates(offset=last_update)

                if not updates.get('result'):
                    continue

                last_update = updates['result'][-1]['update_id'] + 1
                for update in updates['result']:
                    router = BotRouter(json.dumps(update))
                    dispatch(router)
        except KeyboardInterrupt:
            print('===>>>  You stopped polling <<<===')

from datetime import datetime
import pytz
from django.conf import settings
from django.db.models import QuerySet


class MessageQuerySet(QuerySet):
    def create_message(self, data, chat, type):
        type = type or self.model.TYPE_TEXT
        """ Creates botmother Messages """
        tz = pytz.timezone(settings.TIME_ZONE)
        date = datetime.utcfromtimestamp(data.get('date')).replace(tzinfo=tz) if data.get('date') else datetime.now()
        message = self.model(
            chat=chat,
            id=data.get('message_id') or data.get('id'),
            text=data['text'],
            date=date,
            type=type,
        )
        # message.save()

        return message

from django.conf import settings

from botmother.querysets.message import MessageQuerySet
from botmother.querysets.chat import ChatQuerySet
import json
from django.db.models import JSONField
from django.db import models
from django.db.models import CASCADE
from django.utils.translation import ugettext_lazy as _
from botmother.utils.api import TelegramAPI


class Chat(models.Model):
    """ All botmother bot chats (private/group) with there id ( ID is not autoincrement field ) """

    chat_id = models.BigIntegerField()
    type = models.CharField(max_length=255)
    username = models.CharField(max_length=255, null=True, blank=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_action = models.CharField(max_length=255, null=True)
    data = JSONField(null=True)
    last_activity = models.DateTimeField(auto_now_add=True, editable=False, null=True)

    objects = ChatQuerySet.as_manager()

    @property
    def last_data(self):
        return json.loads(self.data or '{}')

    @last_data.setter
    def last_data(self, data):
        self.data = json.dumps(data)

    def send_message(self, text, reply_markup=None, chat_id=None, **kwargs):
        telegram = TelegramAPI(settings.BOT_TOKEN)
        return telegram.send_message(text, chat_id or self.chat_id, reply_markup, **kwargs)

    def send_location(self, lon, lat, reply_markup=None, chat_id=None, **kwargs):
        telegram = TelegramAPI(settings.BOT_TOKEN)
        return telegram.send_location(lon, lat, chat_id or self.chat_id, reply_markup, **kwargs)

    def send_photo(self, photo, reply_markup=None, **kwargs):
        telegram = TelegramAPI(settings.BOT_TOKEN)
        return telegram.send_photo(photo, self.chat_id, reply_markup, **kwargs)

    def forward_message(self, to_chat_id, message_id, reply_markup=None, **kwargs):
        telegram = TelegramAPI(settings.BOT_TOKEN)
        return telegram.forward_message(to_chat_id, self.chat_id, message_id, reply_markup, **kwargs)

    def send_answer_pre_checkout_query(self, id, ok, **kwargs):
        telegram = TelegramAPI(settings.BOT_TOKEN)
        return telegram.send_answer_pre_checkout_query(id, ok, self.chat_id, **kwargs)

    def send_invoice(
            self,
            title,
            description,
            payload,
            provider_token,
            start_parameter,
            currency,
            prices,
            reply_markup=None,
            **kwargs
    ):
        telegram = TelegramAPI(settings.BOT_TOKEN)
        return telegram.send_invoice(
            title,
            description,
            payload,
            provider_token,
            currency,
            prices,
            start_parameter,
            self.chat_id,
            reply_markup,
            **kwargs
        )

    class Meta:
        db_table = 'telegram_chats'


class Message(models.Model):
    """ All botmother bot messages with there id ( ID is not autoincrement field ) """

    TYPE_TEXT = 'text'
    TYPE_CALLBACK = 'callback'
    TYPE_COMMAND = 'command'
    TYPE_LOCATION = 'location'
    TYPE_CONTACT = 'contact'
    TYPE_PHOTO = 'photo'
    TYPE_NEW_MEMBER = 'new_chat_member'
    TYPE_NEW_CHAT_PHOTO = 'new_chat_photo'
    TYPE_PRE_CHECKOUT_QUERY = 'pre_checkout_query'

    id = models.BigIntegerField(_('id'), primary_key=True)
    date = models.DateTimeField()
    chat = models.ForeignKey(Chat, CASCADE, related_name='messages')
    text = models.TextField(null=True, blank=True, verbose_name=_("text"))
    type = models.CharField(max_length=255, default=TYPE_TEXT)

    objects = MessageQuerySet.as_manager()

    def __str__(self):
        return "(%s,%s)" % (self.chat.first_name, self.text or '(no text)')

    class Meta:
        db_table = 'telegram_messages'


class Push(models.Model):
    sms = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False, null=True)
    updated_at = models.DateTimeField(auto_now=True, editable=False, null=True)

    class Meta:
        db_table = 'telegram_push_campaigns'

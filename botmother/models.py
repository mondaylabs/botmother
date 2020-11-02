from django.conf import settings

from botmother.querysets.message import MessageQuerySet
from botmother.querysets.chat import ChatQuerySet
import json
from django.db.models import JSONField, Model
from django.db import models
from django.db.models import CASCADE
from django.utils.translation import ugettext_lazy as _
from botmother.utils.api import TelegramAPI


class Chat(Model, TelegramAPI):
    """ All botmother bot chats (private/group) with there id ( ID is not autoincrement field ) """

    def __init__(self, *args, **kwargs):
        Model.__init__(self, *args, **kwargs)
        TelegramAPI.__init__(self, settings.BOT_TOKEN, self.chat_id)

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

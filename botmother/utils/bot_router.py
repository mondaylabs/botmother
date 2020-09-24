import json

from django.conf import settings

from botmother.models import Message, Chat
from botmother.utils.helpers import action_name
from django.utils import timezone

from botmother.utils.location import location_field
from botmother.utils.string import parse_integer

CONTINUE = 'continue_router_match'


class BotRouter:
    """
    Parses and routes botmother webhook request
    """
    update_id = None
    message = None
    raw_message = {}
    chat = None

    user_location = None
    user_phone = None

    video_note = None
    video = None

    # only on callback query
    callback_data = None
    callback_id = None

    type = None
    runned = False
    is_edit = False
    redirect_action = None
    pre_checkout_query = None

    def __init__(self, request_body):
        """ Parse and set type of botmother webhook request """

        update = json.loads(request_body)
        self.pre_checkout_query = update.get('pre_checkout_query')

        self.update_id = update['update_id']
        self.bot = settings.BOT_TOKEN

        if 'message' in update:
            self._init_message(update['message'])

        elif 'edited_message' in update:
            self.is_edit = True
            self._init_message(update['edited_message'])

        elif 'callback_query' in update:
            self._init_callback(update['callback_query'])

        elif 'pre_checkout_query' in update:
            self._init_message(update['pre_checkout_query'])
            self.chat = Chat.objects.get(chat_id=self.pre_checkout_query.get('from', {}).get('id'))

    def _init_message(self, message):
        self.raw_message = message
        self.chat = Chat.objects.create_chat(message.get('chat') or message.get('from'))

        # check type of webhook request
        self.type = self._type_of_message(message)

        if self.type is Message.TYPE_LOCATION:
            self.user_location = self.raw_message['location']
            self.raw_message['text'] = location_field(self.user_location)

        elif self.type is Message.TYPE_CONTACT:
            self.user_phone = parse_integer(self.raw_message['contact']['phone_number'])
            # save  contact as message text
            self.raw_message['text'] = self.user_phone

        elif self.type is Message.TYPE_PHOTO:
            self.raw_message['text'] = ""

        elif self.type is Message.TYPE_NEW_MEMBER:
            self.raw_message['text'] = self.raw_message['new_chat_member']['first_name']

        elif self.type is Message.TYPE_NEW_CHAT_PHOTO:
            self.raw_message['text'] = ""

        else:
            self.raw_message['text'] = self.raw_message['text'] if 'text' in self.raw_message else ""

        self.message = Message.objects.create_message(self.raw_message, self.chat, type=self.type)

    def _init_callback(self, callback):
        self.type = Message.TYPE_CALLBACK

        if 'message' in callback:
            self.raw_message = callback['message']
            # save  callback data as message text ))))
            self.raw_message['text'] = callback['data']

            # ex: "product_1" to "1"
            self.callback_data = callback['data'].split('_').pop()
            self.callback_id = callback['id']
            self.chat = Chat.objects.create_chat(self.raw_message['chat'])
            self.message = Message.objects.create_message(self.raw_message, self.chat, type=self.type)

    def _type_of_message(self, message):
        if 'text' in message and message['text'].startswith('/'):
            return Message.TYPE_COMMAND
        elif 'text' in message:
            return Message.TYPE_TEXT
        elif 'location' in message:
            return Message.TYPE_LOCATION
        elif 'contact' in message:
            return Message.TYPE_CONTACT
        elif 'photo' in message:
            return Message.TYPE_PHOTO
        elif 'new_chat_member' in message:
            return Message.TYPE_NEW_MEMBER
        elif 'new_chat_photo' in message:
            return Message.TYPE_NEW_CHAT_PHOTO
        elif 'pre_checkout_query' in message:
            return Message.TYPE_PRE_CHECKOUT_QUERY
        else:
            return None

    def command(self, command, function, last_action=None, chat_type=None, edited=False, reply_type=None, extra={}):
        """ Routes command type webhook """
        if self.type != Message.TYPE_COMMAND:
            return

        # command be equals to message text
        if self.message.text == command:
            self.run(function, last_action, chat_type, edited, reply_type, extra)

    def starts_with(self, prefix, function, last_action=None, chat_type=None, edited=False, reply_type=None, extra={}):
        """ Routes text type webhook that starts with given prefix """
        text = self.message.text
        if type(text) == str and text.startswith(prefix):
            self.run(function, last_action, chat_type, edited, reply_type, extra)

    def text(self, text, function, last_action=None, chat_type=None, edited=False, reply_type=None, extra={}):
        """ Routes text type webhook """
        if self.type != Message.TYPE_TEXT:
            return

        # text must be none or equals to message text
        if text is None or text == self.message.text or (isinstance(text, list) and self.message.text in text):
            self.run(function, last_action, chat_type, edited, reply_type, extra)

    def callback(self, prefix, function, last_action=None, chat_type=None, edited=False, reply_type=None, extra={}):
        """ Routes callback type webhook """
        if self.type != Message.TYPE_CALLBACK:
            return

        # prefix must be none or be start of message text
        if prefix is None or self.message.text.startswith(prefix):
            self.run(function, last_action, chat_type, edited, reply_type, extra)

    def location(self, function, last_action=None, chat_type=None, edited=False, reply_type=None, extra={}):
        """ Routes location type webhook to handlers """
        if self.type == Message.TYPE_LOCATION:
            self.run(function, last_action, chat_type, edited, reply_type, extra)

    def contact(self, function, last_action=None, chat_type=None, edited=False, reply_type=None, extra={}):
        """ Routes contact type webhook to handlers """
        if self.type == Message.TYPE_CONTACT:
            self.run(function, last_action, chat_type, edited, reply_type, extra)

    def new_photo(self, function, last_action=None, chat_type=None, edited=False, reply_type=None, extra={}):
        """ Routes to handlers when you add group photo """
        if self.type == Message.TYPE_NEW_CHAT_PHOTO:
            self.run(function, last_action, chat_type, edited, reply_type, extra)

    def any(self, function, last_action=None, chat_type=None, edited=False, reply_type=None, extra={}):
        """ Routes any type of webhook request """
        self.run(function, last_action, chat_type, edited, reply_type, extra)

    def on_checkout_query(self, function, last_action=None, chat_type=None, edited=False, reply_type=None, extra={}):
        """ Routes pre_checkout_query type of webhook request """
        if self.pre_checkout_query:
            self.run(function, last_action, chat_type, edited, reply_type, extra)

    def run(self, function, last_action=None, chat_type=None, edited=False, reply_type=None, extra={}):
        """ Runs handler function """

        if self.runned:
            return

        if self.is_edit and not edited:
            return

        if last_action is not None:
            if callable(last_action) and action_name(last_action) != self.chat.last_action:
                return

            if isinstance(last_action, list) and self.chat.last_action not in [action_name(a) for a in last_action]:
                return

        if chat_type is not None and chat_type not in self.chat.type:
            return

        rt = self._type_of_message(self.raw_message.get('reply_to_message', {}))

        if reply_type is not None and rt != reply_type:
            return

        print('RUNNING HANDLER: ' + function.__name__ + " TYPE: " + self.type if self.type else 'Unknown Type')

        result = function(
            update_id=self.update_id,
            message=self.message,
            message_id=(self.chat.id, self.message.id),
            chat=self.chat,
            redirect=self._redirect,
            location=self.user_location,
            phone=self.user_phone,
            callback_data=self.callback_data,
            callback_id=self.callback_id,
            raw_message=self.raw_message,
            pre_checkout_query=self.pre_checkout_query,
            extra=extra,
        )

        self.runned = result != CONTINUE

        self.chat.last_activity = timezone.now()
        self.chat.save()

    def _redirect(self, action, **kwargs):
        self.redirect_action = action
        action(chat=self.chat, redirect=self._redirect, **kwargs)

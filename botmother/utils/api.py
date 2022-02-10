from io import TextIOWrapper, BufferedReader

from django.conf import settings
import json
import requests
from requests import HTTPError

_test_requests = []


def test_request(index):
    return _test_requests[index]


def clear_test_requests():
    global _test_requests
    _test_requests = []


class TelegramAPI(object):
    def __init__(self, token=None, chat_id=None):
        self.token = token

        if chat_id:
            self.chat_id = chat_id

    def send(self, method, data=None, files=None):
        if settings.TESTING:
            _test_requests.append({'method': method, 'data': data})
            return

        if data and hasattr(self, 'chat_id'):
            data.setdefault('chat_id', self.chat_id)

        if data.get('reply_markup'):
            data['reply_markup'] = json.dumps(data['reply_markup'])
        else:
            data.pop('reply_markup', None)

        try:
            response = requests.post(
                f'https://api.telegram.org/bot{self.token}/{method}?',
                params=data,
                files=files or {}
            )
            response.raise_for_status()
            body = response.json()
        except HTTPError as e:
            body = e.response.json()
            print(body)

        return body

    def send_message(self, text, reply_markup=None, **kwargs):
        return self.send('sendMessage', {
            'text': text,
            'reply_markup': reply_markup,
            **kwargs
        })

    def edit_message(self, text, message_id, reply_markup=None, **kwargs):
        return self.send('editMessageText', {
            'text': text,
            'message_id': message_id,
            'reply_markup': reply_markup,
            **kwargs
        })

    def delete_message(self, message_id, **kwargs):
        return self.send('deleteMessage', {
            'message_id': message_id,
            **kwargs
        })

    def send_location(self, lon, lat, reply_markup=None, **kwargs):
        return self.send('sendLocation', {
            'longitude': lon,
            'latitude': lat,
            'reply_markup': reply_markup,
            **kwargs
        })

    def forward_message(self, to_chat_id, from_chat_id, message_id, **kwargs):
        return self.send('forwardMessage', {
            'chat_id': to_chat_id,
            'from_chat_id': from_chat_id,
            'message_id': message_id,
            **kwargs
        })

    def send_photo(self, photo, reply_markup=None, **kwargs):
        return self.send('sendPhoto', {
            'photo': photo,
            'reply_markup': reply_markup,
            **kwargs
        })

    def send_document(self, document, reply_markup=None, **kwargs):
        files = None
        data = {'reply_markup': reply_markup, **kwargs}
        if type(document) in (TextIOWrapper, BufferedReader):
            files = {'document': document}
        else:
            data['document'] = document

        return self.send('sendDocument', data, files=files)

    def send_answer_pre_checkout_query(self, id, ok, **kwargs):
        return self.send('answerPreCheckoutQuery', {
            'ok': ok,
            'pre_checkout_query_id': id,
            **kwargs
        })

    def send_invoice(
            self,
            title,
            description,
            payload,
            provider_token,
            currency,
            prices,
            start_parameter,
            reply_markup=None,
            **kwargs
    ):
        return self.send('sendInvoice', {
            'title': title,
            'description': description,
            'start_parameter': start_parameter,
            'provider_token': provider_token,
            'currency': currency,
            'prices': json.dumps(prices),
            'payload': payload,
            'reply_markup': reply_markup,
            **kwargs
        })

    def send_chat_action(self, action='typing', **kwargs):
        return self.send('sendChatAction', {
            'action': action,
            **kwargs
        })

    def get_updates(self, **kwargs):
        return self.send('getUpdates', {
            **kwargs
        })

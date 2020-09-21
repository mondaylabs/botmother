from django.conf import settings
import json
from urllib.error import HTTPError
from urllib.request import urlopen, Request

_test_requests = []


def test_request(index):
    return _test_requests[index]


def clear_test_requests():
    global _test_requests
    _test_requests = []


class TelegramAPI:
    def __init__(self, token):
        self.token = token

    def send(self, method, data):
        if settings.TESTING:
            _test_requests.append({'method': method, 'data': data})
            return

        if 'reply_markup' in data and data['reply_markup'] is None:
            del data['reply_markup']

        try:
            body = urlopen(Request(
                f'https://api.telegram.org/bot{self.token}/{method}',
                json.dumps(data).encode(),
                headers={'Accept': 'application/json', 'Content-Type': 'application/json'},
            )).read().decode()
        except HTTPError as e:
            body = e.read().decode()
            print(body)

        return json.loads(body)

    def send_message(self, text, chat_id, reply_markup=None, **kwargs):
        reply_markup = json.dumps(reply_markup) if reply_markup else None
        return self.send('sendMessage', {
            'chat_id': chat_id,
            'text': text,
            'reply_markup': reply_markup,
            **kwargs
        })

    def send_location(self, lon, lat, chat_id, reply_markup=None, **kwargs):
        reply_markup = json.dumps(reply_markup) if reply_markup else None
        return self.send('sendLocation', {
            'chat_id': chat_id,
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

    def send_photo(self, photo, chat_id, reply_markup=None, **kwargs):
        reply_markup = json.dumps(reply_markup) if reply_markup else None
        return self.send('sendPhoto', {
            'chat_id': chat_id,
            'photo': photo,
            'reply_markup': reply_markup,
            **kwargs
        })

    def send_answer_pre_checkout_query(self, id, ok, chat_id, **kwargs):
        return self.send('answerPreCheckoutQuery', {
            'chat_id': chat_id,
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
            chat_id,
            reply_markup=None,
            **kwargs
    ):
        reply_markup = json.dumps(reply_markup) if reply_markup else None
        return self.send('sendInvoice', {
            'chat_id': chat_id,
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

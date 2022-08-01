
import json


# ordinary keyboard
def keyboard(buttons, **kwargs):
    return {'keyboard': buttons, 'resize_keyboard': True, **kwargs}


def button(text, location=None, contact=None, **kwargs):
    data = {'text': text, **kwargs}

    if location:
        data['request_location'] = True

    if contact:
        data['request_contact'] = True

    return data


# inline keyboard
def inline_keyboard(callback_buttons, **kwargs):
    return {'inline_keyboard': callback_buttons, 'resize_keyboard': True, **kwargs}


def inline(text, data, key, **kwargs):
    assert isinstance(data, dict)
    return {'text': text, 'callback_data': f"{key}--{json.dumps(data)}", **kwargs}

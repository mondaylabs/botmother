
import json

# ordinary keyboard
def keyboard(buttons):
    return {'keyboard': buttons, 'resize_keyboard': True}


def button(text, location=None, contact=None):
    data = {'text': text}

    if location:
        data['request_location'] = True

    if contact:
        data['request_contact'] = True

    return data

# inline keyboard
def inline_keyboard(callback_buttons):
    return {'inline_keyboard': callback_buttons, 'resize_keyboard': True}


def inline(text, data, key):
    assert isinstance(data, dict)
    return {'text': text, 'callback_data': f"{key}--{json.dumps(data)}"}

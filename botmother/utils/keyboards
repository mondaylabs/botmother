# inline keyboard
def inline_keyboard(inline_keyboard_name):
    return {'inline_keyboard': inline_keyboard_name, 'resize_keyboard': True}


def inline(text, data, key):
    return {'text': text, 'callback_data': f"{key}--{json.dumps(data)}"}


# ordinary keyboard
def keyboard(keyboard_name):
    return {'keyboard': keyboard_name, 'resize_keyboard': True}


def button(text, location=None, contact=None):
    data = {'text': text}

    if location:
        data['request_location'] = True

    if contact:
        data['request_contact'] = True

    return data

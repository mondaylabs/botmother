def start(chat, no_text=False, **kwargs):
    if no_text:
        return

    chat.send_message('Hi'.format(name=chat.first_name))

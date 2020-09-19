def start(chat, **kwargs):
    chat.send_message('Hi'.format(name=chat.first_name))

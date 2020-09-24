from botmother.utils.bot_router import CONTINUE


def start(chat, **kwargs):
    chat.send_message('Hi {name}'.format(name=chat.first_name))
    return CONTINUE


def menu(chat, **kwargs):
    chat.send_message('I am a Botmother for creating telegram bots')

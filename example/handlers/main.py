from botmother.utils.bot_router import CONTINUE


def start(chat, redirect, **kwargs):
    chat.send_message('Hi {name}'.format(name=chat.first_name))
    kwargs['extra'] = {}
    redirect(menu, **kwargs)
    return CONTINUE


def menu(chat, **kwargs):
    chat.send_message('I am a Botmother for creating telegram bots')



def start(chat, redirect, **kwargs):
    chat.send_message('Hi {name}'.format(name=chat.first_name))
    kwargs['extra'] = {}
    redirect(menu, **kwargs)


def menu(chat, **kwargs):
    chat.send_message('I am a BotMother for creating telegram bots')

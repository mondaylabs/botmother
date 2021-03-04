from botmother.utils.keyboards import *


def main_menu():
    return keyboard([
        [button('Да'), button('Нет')],
        [button('Не знаю')]
    ])


def inline_menu():
    return inline_keyboard([
        [inline('I am fine!', {'value': True}, 'is-chosen')],
        [inline('I am sad!', {'value': False}, 'is-chosen')]
    ])


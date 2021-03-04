# Телеграм-бот на Python


Библиотека телеграм бота на Django


> БИБЛИОТЕКА НАХОДИТСЯ НА СТАДИИ РАЗРАБОТКИ. ИСПОЛЬЗОВАТЬ ЕЕ ПОКА НЕ РЕКОМЕНДУЕТСЯ.

Описание
-----------
Библиотека BotMother построена на Django. В свою очередь, библиотека предназначена для создания разноуровневых ботов, начиная от инфомативных и заканчивая до онлайн-магазинов. Плюсы библиотеки заключаются в ее фунциональности и простоте понимания, посредством использования распространенных полезных функций. Далее будет подробно разобраны примеры применения функций BotMother. 

Зависимости
-----------
1.	Python 3 
2.	Django последней версии
3.	Ngrok – можете установить и почитать документацию по [ссылке](https://ngrok.com/download) 
4. psycopg2 (2.8.6)


Установка
-----------
 1. Запустите команду:
 * http - `pip install git+https://github.com/mondaylabs/botmother.git@v0.4.0`
 * ssh  - `pip install git+ssh://git@github.com/mondaylabs/botmother.git@v0.4.0`

Библиотека установлена, идем дальше.

2. Откройте файл `settings.py` и добавьте в `INSTALLED_APPS` название библиотеки и вашего приложения:
```python
INSTALLED_APPS = [
    ...
    'botmother',
    'имя_вашего_приложения'
]
```

3. Создайте нового бота с помощью [BotFather]( @BotFather). Скопируйте токен созданного бота и задайте его в переменной `BOT_TOKEN` в том же `settings.py`: 
```python
BOT_TOKEN = '1619688226:AAFa1v1nPZXWG97wFdu4W**************'
```
4. Также, добавьте следующее:

```python
	import sys
	...	
	BOTMOTHER_CHAT_MODEL = 'botmother.Chat'
	TESTING = ('test' == sys.argv[1]) if sys.argv else False
```
5.  Далее, для того, чтобы ваш бот правильно работал, вам следует создать модель `Chat` в `models.py`. 
```python
from botmother.models import AbstractChat

class Chat(AbstractChat):
    class Meta(AbstractChat.Meta):
        db_table = '<имя_вашего_приложения>_chats'
```
Еще пару очень важных моментов:

`Chat` модель должна наследоваться от `AbstractChat` класса, та в свою очередь наследуется от `TelegramAPI` класса.
`AbstractChat`  уже имеет следующие переменные, такие как:  `chat_id, type, username, first_name, last_action, data, last_activity`.

Как видно выше, `AbstractChat` класс уже имеет достаточное количество переменных, которые могут быть полезны. Их не обязательно прописывать в своих моделях. 
Вам просто нужно импортировать `AbstractChat` и прописать его в наследство созданной вами модели.

6. Перейдя в командную строку, пропишите команду `python manage.py makemigrations` и `python manage.py migrate`.
После этого, просто поменяйте `BOTMOTHER_CHAT_MODEL = 'botmother.Chat'` на `BOTMOTHER_CHAT_MODEL = '<название_вашего_приложения>.Chat'`

7. Создайте файл `handlers.py` в папке приложения и напишите свою первую функцию `start`:
```python
def start(chat, *args, **kwargs):
    chat.send_message('Hello, world!')
```

8. Создайте файл `urls.py` в папке вашего приложения так, чтобы у вас получился путь `<имя_вашего_проекта >/<имя_вашего_приложения>/urls.py`, и добавьте функцию `dispatch()`, как показано ниже:
```python
from botmother.webhook import webhook
from django.urls import path
from example.handlers.main import *


def dispatch(router):
    router.command('/start', start),

urlpatterns = [
    path('webhook', webhook(dispatch)),
],
```
Теперь, перейдите в корневой файл urls.py и выполните следующие действия:
```python
urlpatterns = [
    ...
    path('example/', include(('example.urls', 'example'), namespace='example')),
]
```
Вместо `example` вы должны подставить имя своего приложения.

9.	Так же добавьте `ngrok` в `ALLOWED_HOSTS` следующим образом:
```python
ALLOWED_HOSTS = (
    ...
    '.ngrok.io',
)
```

10.	Запустите ngrok командой `ngrok http 8000`.
Но прежде, укажите где находится файл `ngrok.exe` в командной строке. Затем, скопируйте появившуюся ссылку, показанную ниже:

    `Forwarding                    https://82691332ba1f.ngrok.io -> http://localhost:8000`

11. Добавив `/example/webhook` в конец ссылки, запустите `webhook` командой:

    `py manage.py setwebhook https://82691332ba1f.ngrok.io/example/webhook`

12.	Запустите бота командой `py manage.py runserver`.

13.	Проверьте работоспособность своего бота!


Функции bot_router.py
-----------
Еще один важный момент, который поможет лучше понять, как работает `BotMother` это функции в корневом файле `bot_router.py` (можете почитать по [ссылке](https://github.com/mondaylabs/botmother/blob/master/botmother/utils/bot_router.py)).
Все функции, в обязательном порядке, принимают аргумент `function` в виде обработчиков.
Сейчас я поочередно опишу каждую функцию:
* `сommand`   - Обязательный аргумент: `command,  function`. Нужна для обработки команд бота, таких как `/start`. Другие типы сообщений эта команда не принимает.
* `starts_with` - Обязательный аргумент: `prefix, function`. Направляет веб-перехватчик текстового типа, который начинается с заданного префикса.
* `text` - Обязательный аргумент: `text, function`. Отвечает только за текстовые команды. 
* `any` – Обязательный аргумент: `function`. Отвечает на любые типы данных.
* `callback` – Обязательный аргумент: `prefix, function`. Нужна при создании `inline` кнопок. Эта функция отправляет `callback` для дальнейшей обработки и ответа пользователю.
* `location` – Обязательный аргумент: `function`. Обрабатывает местоположение.
* `contact` – Обязательный аргумент: `function`. Обрабатывает контакт.
* `on_checkout_query` – Обязательный аргумент: `function`. Полезная функция при написании бота для онлайн-магазина. Данная функция может служить направляющей для дальнейшей оплаты или каких-либо других действий.
* `new_photo` – Обязательный аргумент: `function`. Перенапрявляет в функцию и при добавлении группового фото.

Все функции принимают необязательные аргументы, как: 
* `last_action` - самый полезное свойство, которое поможет прописать поочередность выполнения обработчиков.
* `chat_type` - private, group, supergroup, channel`. Если вы пишите чат-бота, то он будет работать в личной переписке.С другими работает аналогично.
* `edited` - сообщит боту изменено ли клиентом сообщение.
* `extra`  - можно прописать специфические данные, которые потом можно передать в хендлеры.



Инструкция по `handlers.py` и `models.py`. 
Описание самых важных функций
-----------
Хендлеры – это функция, которая вызывается какой-либо программной системой в ответ на наступление какого-либо события. Их еще называют обработчиками. Следственно, можно понять, что они и будут выполнять всю работу вашего бота. Но, что бы они начали работать, нужно ознакомиться с функциями `BotMother`, которые помогут эти обработчики правильно прописать и связать.
 
При написании хендлеров, не стоит забывать о обязательных атрибутах, без которых ваша функция может не работать:

* `message` – обязательный атрибут, является экземпляром модели `Message`.
* `chat` – самый главный атрибут, нужен для взаимодействия с клиентом. Тоже является экземпляром модели `Chat`. 
* `redirect` –  перенаправит на другую функцию после выполнения предыдущей. Обязательно пропишите ее в качестве аргумента в вашей функции. Далее укажите в `redirect` в качестве аргумента функцию, на которую вы хотите перейти.
* `location`  - нужен для обработки локации, отправленной клиентом.
* `phone` -  нужен для обработки контакта.
* `callback_data` – обязательный атрибут при `inline`-клавиатурах. После нажатия, бот должен получить запрос на обработку данных и выполнения
соответствующей функции. Этот запрос должен содержать `callback_data`. Он может быть не виден клиенту, но обязателен к внесению.
* `pre_checkout_query` – полезный атрибут для online-магазинов. Выполнит указанные действия, прописанные в этом атрибуте.
* `extra` – полезный атрибут при разграничении схожих функций.

Пропишите необходимые для работы атрибуты и `*args, **kwargs` в конце:
```python
def start(chat, *args, **kwargs):
    chat.send_message('Hello, world')
```
В BotMother существует полезная константа `CONTINUE`. Как вы уже знаете, `BotMother` делает обход функций пока не найдет нужной, после чего выполнит его и выведет результат.  
Константа `CONTINUE` может помочь продолжить обход, даже после выполнения указанной функции. Например:

Без константы `CONTINUE`

`#> Пользователь ввел "Привет"`
```python
from .handlers import *

router.text('Привет', first_func)  # <-- Запуск функции без продолжения обхода , выведение результата и остановка.
router.text(None, second_func) 
```

С константой `CONTINUE`

`#> Пользователь ввел "Привет"`

```python
from .handlers import *

router.text('Привет', hadlers.first_func)  # <--  Запуск функции c последующим продолжением обхода.
router.text('Hello', hadlers.second_func)  
router.text('Guten Tag', hadlers.third_func)
router.starts_with('П', hadlers.fourth_func)  # <--- Второй запуск функции.
```
Рассмотрим модели `BotMother`:
1.	`class AbstractChat(Model, TelegramAPI)` – как было указано выше, ваш `class Chat` наследуется от `AbstractChat`. В свою очередь, `AbstractChat` наследуется от `TelegramAPI`. 
`AbstractChat` уже имеет следующие переменные: `chat_id, type, username, first_name, last_action, last_activity`. 

    И свойство `last_data`, которое временно присвоит значение какой либо переменной. 
    Для полного понимания, разберем пример. Допустим, вы создаете бота-опросника, бот задает 4-5 или больше вопросов, клиент, не ответив на все вопросы, закрывает бота. А что с данными? Естественно они сохранятся в базе данных, занимая нужную вам память. Так вот, во избежание этого BotMother использует `last_data`. Это свойство тоже использует вашу базу данных, но данные будут полностью внесены только после завершения всех прописанных вами действий. Оно вам поможет временно сохранить данные и избежать нагрузки. Сначала это может показаться незначительным. Но при создании больших проектов, разница будет ощутима.

    От `TelegramAPI` наша модель наследует следующие функции: 
* `send` – отправит данные в любом виде
* `send_message` – самая нужная и распространенная функция. С ней вы будете работать постоянно. Она будет отправлять данные только в текстовом виде. 
Также, она принимает в качестве аргумента `reply_markup`, что говорит о возможности отправки клавиатуры:
```python
chat.send_message('Choose the language: ', reply_markup=keyboard_name())
```
* `edit_message` - редактирует отправленное ботом сообщение. Рассмотрим на примере:

```python 
def menu(chat, redirect, message, **kwargs):
    response = chat.send_message('I am a BotMother for creating telegram bots. Write smth ')
    chat.last_data = {'message_id': response.get('result', {}).get('message_id')}

def change(chat, *args, **kwargs):
    chat.edit_message('Nice to meet ya!', message_id=chat.last_data.get('message_id'))
```
1. Сначала необходимо внести данные сообщения в любую переменную (например `response`).
2. Затем вытащить `message_id` сообщения для дальнейшего редактирования. 
3. В обязательном порядке, нужно сохранить эти данные в `last_data`, в виде словаря.
4. Главными атрибутами функции являются `text` и `message_id`. Поэтому, в следующей функции, в атрибуте `message_id`, необходимо вытащить с `last_data` данные      		`message_id` и прописать, как показано выше.
* `send_location, send_photo` – соответственно отправляет пользователю местоположение или фото. 
* `send_answer_pre_checkout_query` – Важная функция для онлайн-магазина. Проверяет правильность оплаты за продукт и отправляет сообщение, или же запускает какую-либо функцию после выполнения функции оплаты. 
* `send_invoice` – отправляет «чек» или опять же запускает вашу функцию, уведомляющую клиента о успешном снятии денег.
* `delete_message` - удаляет выбранное сообщение. Пример:
```python
def start(chat, redirect, message, **kwargs):
    response = chat.send_message('Hello world!')
    chat.last_data = {'message_id': response.get('result', {}).get('message_id')}

def delete(chat, message, *args, **kwargs):
    if message:
        chat.delete_message( message_id=chat.last_data.get('message_id'))
```
Как вы могли заметить `delete_message` схож с `edit_message` тем, что требует `message_id` . Единственная разница это отсутствие обязательного атрибута `text`.

Рекомендации
-----------
В этой части будут даны советы по успешному и правильному использованию библиотеки, грамотному использованию функций и построению иерархии бота:

1.	Начнем самого малого. Для дальнейшей гибкости вашего бота, следует прописать свою  `Chat` модель в `models.py`.

`models.py` библиотеки `BotMother` имеет `class AbstractChat`. Абстрактный метод – это метод, который не имеет своей реализации в базовом классе, и он должен быть реализован в классе-наследнике.
Поэтому вам в обязательном порядке нужно создать свою модель. Таким образом, вы можете добавить необходимые вам переменные. Обязательно пропишите в модели аргумент AbstractChat. Этим вы унаследуете уже существующие переменные:
```python
class Chat(AbstractChat):
    class Meta(AbstractChat.Meta):
        db_table = '<имя_вашего_приложения>_chats'
```
После написания модели, обязательно укажите это в `settings.py`:
```python
...
BOTMOTHER_CHAT_MODEL = '< имя_вашего_приложения>.Chat'
```
2.	Продолжая тему создания клавиатуры, хочется добавить, что необходимо, в первую очередь, эту клавиатуру создать. Сейчас будет пошагово разобрано, как можно создать простую клавиатуру:
* Создаем файл keyboards.py в папке приложения. 
* Далее копируем и вставляем нижепоказанный код:
```python
from botmother.utils.keyboards import *

def main_menu():
    return keyboard([
        [button('Хорошо'), button('Не очень!')],
        [button('Назад')]
    ])
```
`Botmother` уже имеет встроенные функции по созданию клавиатуры -  `keyboard()` и кнопок - `button()`. Вам остается только прописать внутренний текст, так как это обязательный атрибут.

* Напишите функцию в `handlers.py` для обработки ответа клавиатуры :
```python
from example.keyboards import *
    
def start(chat, **kwargs):
    chat.send_message('I am a BotMother for creating telegram bots')
    chat.send_message('Как дела?', reply_markup=main_menu()))

def answer(chat, message, *args, **kwargs):
    message = message.text
    if message === 'Да':
            chat.send_message('Отлично!')
    else:
            chat.send_message('Плохо!')
```
К сведению, можно назначить какую-либо кнопку отправителем вашего контакта или местоположения:
```python
from botmother.utils.keyboards import *

def main_menu():
    return keyboard([
        [button('Share the contact', contact=True), 
        button('Share location', location=True)],
        [button('Назад')]
    ])
```
3. Создание `inline`-клавиатуры происходит немного иначе:
* Перейдите в `keyboards.py` и добавьте следующее:
```python
from botmother.utils.keyboards import *

def inline_menu(*args, **kwargs):
    return inline_keyboard([
        [inline('I am fine!', {'value': True}, 'is-chosen')],
        [inline('I am sad!', {'value': False}, 'is-chosen')]
    ])
```
Как вы, наверно, уже знаете, `inline`-клавиатура возвращает `callback-data`, что немного отличает ее от простой клавиатуры. 
Как показано выше, `inline_keyboard` на входе принимает параметр `callback_buttons`. Соответственно, необходимо прописать их листами внутри листа (`arrays in array`). Сама функция `inline()` схожа с `button()`, но принимает 3 обязательных параметра: `text`, `data`, `key`:

`text` - содержимое кнопки.

`data` - результат нажатия определенной кнопки в виде словаря.

`key` - префикс необходимый как в `handlers.py` так и в `urls.py`. Далее будет показан наглядный пример.

* Перейдите в `handlers.py`:
```python
from example.keyboards import *
    
def start(chat, **kwargs):
    chat.send_message('I am a BotMother for creating telegram bots')
    chat.send_message('How are you?', 
    reply_markup=inline_menu('is-chosen'))) # key is required

def menu(chat, callback_data, *args, **kwargs):
        chat.send_message('Cool!' if callback_data.get('value')  else 'Why so sad?') #data is required
```
Несколько важных моментов:
- Атрибут `key` должен быть прописан в атрибуте клавиатуры.
- Функция-обработчик ответа клавиатуры должен принимать атрибут `callback_data`, который конвертирован в `JSON`-формат.
- Для ответа вы должны взять именно `data`, который указали в `keyboards.py`.
* Наконец, перейдите в `urls.py` приложения и добавьте нижеизложенное:
```python
from botmother.webhook import webhook
from django.urls import path
from example.handlers import main

def dispatch(router):
    ...
    router.callback('is-chosen', main.menu)

urlpatterns = [
    path('webhook', webhook(dispatch)),
]
```
Как видно выше, первым атрибутом задан `key`, который выступает в роли `prefix`.

4. В `urls.py`, в обязательном порядке, первой должна быть ссылка на `/start` функцию, ибо работа любого бота начинается с этой команды. 
5. Для контроля последовательности выполнения функций, следует так же прописать в ссылках `urls.py` атрибут `last_action`. В ней может быть как 1 переменная, так и несколько, внесенных в свою очередь в список:
```python
router.command('/<your_command>', <func4>, last_action=[<func1>, <func2>, <func3>, <func4>])
```
Это может предотвратить случаи неверной последовательности запуска обработчиков.

6.	Немаловажный момент это сохранение поэтапности функций. Если вы пишете, например, бота-опросника, то верным решением будет сначала прописывать сам вопрос, а затем, в следующей функции, его обрабатывать  и продолжить по цепочке. Например:
```python
def start(chat, *args, **kwargs):
    chat.send_message(‘What is your name?’)
    
def ask_name(chat, *args, **kwargs ):
    name = message.text
    #ловите запрос от первой функции и обрабатываете
    chat.send_message(f‘Ok, {name}. How old are you?’)
    
def ask_age(chat, *args, **kwargs ):
    age = message.text
    #ловите запрос от второй функции и обрабатываете
    chat.send_message(f‘Oh, {name}. Welldone! You are already {age} years old!’)
```
7. Кроме как использования предустановленных команд, вы можете добавить свои собственные. Польза от этого заключается в том, что у вас появится возможность взаимодействовать с приложениям прямо из вашей командной строки. 
 Итак, давайте создадим команду для бота-синоптика, который спросит у зарегистрированных пользваотелей, не хоят ли они узнать погоду:
* Внутри папки своего приложения создайте Python-дерикторию "management", а внутри него "commands".
В commands создайте питоновский файл и дайте ему любое имя. У вас должен получится следующий путь:
`<название_проэкта>/<название_приложения>/management/commands/<файл_с_кодом_команды>`
* В файле создайте `class Command`, унаследовав его от `BaseCommand`. А внутри класса пропишите функцию, которая и будет выполнять рассылку:
```python
from django.core.management.base import BaseCommand
from core.models import Chat


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        chats = Chat.objects.all()   #берем список всех зарегистрированных пользователей
        for chat in chats:    #делаем обход
            chat.send_message(
                f'{chat.first_name}, как дела? Не желаете узнать погоду? Отправьте команду /<command1>. Если хотите поменять язык, введите команду /<command2>',
                parse_mode="markdown",
            )
```

В командной строке вызовите команду `py manage.py <название_вашего_файла_с_командой>`

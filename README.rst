=====
Monday Labs Python Telegram Patch
=====

This is a Telegram library for creating bots with Django

Quick start
-----------

1. Clone BotMather installs with command (
        * for http - pip install git+https://github.com/mondaylabs/botmother.git@v0.0.7
        * for ssh  - pip install git+ssh://git@github.com/mondaylabs/botmother.git@v0.0.7
    )

2. Add "botMother" to your INSTALLED_APPS setting like this and BOT_TOKEN to settings_dev::

    INSTALLED_APPS = [
        ...
        'botMother',
    ]

    BOT_TOKEN = '1381661048:AAGykSLTZifIkQD79fDOTxQb9kaVTZ1S_-2'

3. Create a function in urls.po and bind it in with the help of path::

    def dispatch(router):
    router.command('/start', main.start)


    urlpatterns = [
        path('', webhook(dispatch)),
    ],

4. Run ``python manage.py migrate`` to create the telegram models.

5. Run ``ngrok`` copy https://url.

6. Run ``python manage.py set_webhook``.

7. Run ``python manage.py runserver``.

8. Join the boot and paste command /start

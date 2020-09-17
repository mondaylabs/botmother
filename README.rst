=====
Monday Labs Python Telegram Patch
=====

This is a Telegram library for creating bots with Django

Quick start
-----------

1. Add "telegram" to your INSTALLED_APPS setting like this and BOT_TOKEN to settings_dev::

    INSTALLED_APPS = [
        ...
        'telegram',
    ]

    BOT_TOKEN = '1381661048:AAGykSLTZifIkQD79fDOTxQb9kaVTZ1S_-2'

2. Create a function in urls.po and bind it in with the help of path::

    def dispatch(router):
    router.command('/start', main.start)


    urlpatterns = [
        path('', webhook(dispatch)),
    ],

3. Run ``python manage.py migrate`` to create the telegram models.

4. Run ``ngrok`` copy https://url.

5. Run ``python manage.py set_webhook``.

6. Run ``python manage.py runserver``.

7. Join the boot and paste command /start

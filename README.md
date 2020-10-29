# Python Telegram bot


This is a Telegram bot library for Django


> THIS LIBRARY IS NOT PRODUCTION READY! PLEASE DON'T USE IT YET!

Quick start
-----------

1. Install it by running
 * http - `pip install git+https://github.com/mondaylabs/botmother.git@v0.2.4`
 * ssh  - `pip install git+ssh://git@github.com/mondaylabs/botmother.git@v0.2.4`

2. Add "botMother" to your INSTALLED_APPS setting like this and BOT_TOKEN to settings_dev:  

```python
INSTALLED_APPS = [
    ...
    'botMother',
]

BOT_TOKEN = '<bots token>'
```

3. Add router function:  

```python
def dispatch(router):
    router.command('/start', main.start)


urlpatterns = [
    path('', webhook(dispatch)),
],
```

4. Run `python manage.py migrate`.

5. Run `ngrok` copy url `https://***.ngrok.io`.

6. Run `python manage.py set_webhook https://***.ngrok.io`.

7. Run ``python manage.py runserver``.

8. Check your telegram bot!

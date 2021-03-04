from botmother.webhook import webhook
from django.urls import path
from example.handlers import main


def dispatch(router):
    router.command('/start', main.start, extra={'back': True})
    router.callback('is-chosen', main.last)
    router.any(main.unknown)


urlpatterns = [
    path('webhook', webhook(dispatch)),
]


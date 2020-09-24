from botmother.webhook import webhook
from django.urls import path
from example.handlers import main


def dispatch(router):
    router.command('/start', main.start)
    router.any(main.menu)


urlpatterns = [
    path('', webhook(dispatch)),
]

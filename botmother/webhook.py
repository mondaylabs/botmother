from django.conf import settings

from botmother.utils.bot_router import BotRouter
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


def webhook(dispatch):
    @csrf_exempt
    def _view(request):
        try:
            dispatch(BotRouter(request.body.decode("utf-8")))
        except Exception as error:
            if settings.DEBUG:
                raise error
            print(error)

        return JsonResponse({'ok': True})

    return _view

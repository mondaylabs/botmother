from botmother.utils.bot_router import BotRouter
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


def webhook(dispatch):
    @csrf_exempt
    def _view(request):
        try:
            dispatch(BotRouter(request.body.decode("utf-8")))
        except Exception as error:
            print(error)
            import logging

            logger = logging.getLogger(__name__)
            logger.error(error)

        return JsonResponse({'ok': True})

    return _view

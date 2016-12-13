import logging
import requests
from django.conf import settings
from django.http import HttpResponse


logger = logging.getLogger(__name__)


def webhook(request):
    if request.method.lower() == 'get':
        if request.GET.get('hub.mode') == 'subscribe':
            if request.GET.get('hub.verify_token') == settings.FACEBOOK_APP_VERIFICATION_TOKEN:
                return HttpResponse(request.GET.get('hub.challenge'))
            else:
                logger.error('Invalid verify_token in {request.GET}'.format(request=request))
                return HttpResponse(status=403)
        else:
            logger.error('Invalid hub.mode in {request.GET}'.format(request=request))

        return HttpResponse(status=404)

    elif request.method.lower() == 'post':
        data = {
            "recipient": {"id": 'robert.kolner'},
            "message": {"text": 'Hello world!'}
        }
        access_token = settings.FACEBOOK_APP_ACCESS_TOKEN
        response = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + access_token, json=data)
        print(response.content)

    else:
        return HttpResponse('Invalid method', status=400)

import json
import logging

from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from messenger_bot.send_api import send_question, send_text, TYPE_ANSWER, get_user_profile

logger = logging.getLogger(__name__)


def _received_message(event):
    # TODO: Logic!
    text = 'Regjeringen vil gi reservasjonsmuligheter for fastleger etter dialog med Den norske legeforening, jf samarbeidsavtalen.'
    question = {
        'id': 12817,
        'text': text
    }
    return send_question(event['sender']['id'], question)


def _received_postback(event):
    payload = json.loads(event['postback']['payload'])
    if payload.get('type') == TYPE_ANSWER:
        logger.warning("Got answer: {payload[answer]}".format(payload=payload))

    first_name = get_user_profile(event['sender']['id'])['first_name']
    positive = '' if payload['answer'] else ' ikke'
    text = 'Takk {first_name}. Du har{positive} trua.'.format(first_name=first_name, positive=positive)
    return send_text(event['sender']['id'], text)


@csrf_exempt
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
        post_data = json.loads(request.body.decode('utf-8'))

        for entry in post_data['entry']:
            for event in entry['messaging']:
                if event.get('message'):
                    response = _received_message(event)
                elif event.get('postback'):
                    response = _received_postback(event)
                else:
                    response = None
                    logger.warning("Webhook received unknown event: {event}".format(event=event))

                if response is not None:
                    logger.info('Got response: {response}'.format(response=response))

        return HttpResponse('OK', status=200)

    else:
        return HttpResponse('Invalid method', status=400)

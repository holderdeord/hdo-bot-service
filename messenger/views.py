import json
import logging
from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from messenger.api import update_profile
from messenger.handlers import received_event
from messenger.intent_formatters import format_bot_profile

logger = logging.getLogger(__name__)


@csrf_exempt
def webhook(request: HttpRequest):
    if request.method.lower() == 'get':
        # Subscribe webhook and verify token
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

        # Handle webhook request of type message and postback
        # Note: Multiple entries can i batched in one requests and should be handled individually
        # Ref: https://developers.facebook.com/docs/messenger-platform/webhook-reference#format
        for entry in post_data['entry']:
            for event in entry['messaging']:
                if any(key in event for key in ['message', 'postback']):
                    received_event(event)
                else:
                    logger.warning("Webhook received unknown event: {event}".format(event=event))

        return HttpResponse('OK', status=200)
    else:
        return HttpResponse('Invalid method', status=400)


class AdminActionsView(TemplateView):
    template_name = 'messenger/actions.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'app_id': settings.FACEBOOK_APP_ID,
            'page_id': settings.FACEBOOK_PAGE_ID,
        })
        return context


def bot_profile_update(request):
    if request.method == 'POST':
        update_profile(format_bot_profile())

    return redirect('messenger:admin-actions')

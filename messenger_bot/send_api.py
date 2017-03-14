import logging
import requests
from django.conf import settings

logger = logging.getLogger(__name__)


def send_message(data):
    access_token = settings.FACEBOOK_APP_ACCESS_TOKEN
    response = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + access_token, json=data)
    res = response.json()

    if res is not None:
        logger.info('Got response: {response}'.format(response=res))

    return res

import logging
import requests
from django.conf import settings


logger = logging.getLogger(__name__)


API_URL = 'https://graph.facebook.com/v2.6'


def _send_request(url, params, data):
    response = requests.post(url, params=params, json=data)
    res = response.json()

    if res is not None:
        logger.info('Got response: {response}'.format(response=res))

    return res


def get_user_profile(user_id):
    params = {
        'fields': 'first_name',  # , last_name, profile_pic, locale, timezone, gender,
        'access_token': settings.FACEBOOK_APP_ACCESS_TOKEN
    }
    url = '{api_url}/{user_id}/'.format(api_url=API_URL, user_id=user_id)

    response = requests.get(url, params)

    return response.json()


def update_profile(data):
    params = {'access_token': settings.FACEBOOK_APP_ACCESS_TOKEN}
    url = '{api_url}/me/messenger_profile'.format(api_url=API_URL)

    return _send_request(url, params, data)


# Send API
def send_message(data):
    params = {'access_token': settings.FACEBOOK_APP_ACCESS_TOKEN}
    url = '{api_url}/me/messages'.format(api_url=API_URL)

    return _send_request(url, params, data)

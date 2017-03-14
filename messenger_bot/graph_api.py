import requests
from django.conf import settings


def get_user_profile(user_id):
    params = {
        'fields': 'first_name',  # ,last_name,profile_pic, locale, timezone,gender',
        'access_token': settings.FACEBOOK_APP_ACCESS_TOKEN
    }
    url = 'https://graph.facebook.com/v2.6/{user_id}/'.format(user_id=user_id)

    response = requests.get(url, params)

    return response.json()

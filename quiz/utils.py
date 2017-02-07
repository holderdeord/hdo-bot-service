import requests
from django.conf import settings

from quiz.models import GoogleProfile


def get_google_sheet_data():
    """ Ref: https://github.com/google/oauth2client/blob/master/oauth2client/contrib/django_util/__init__.py#L188
        Ref: https://github.com/google/oauth2client/tree/master/samples/django/django_user
    """
    access_token = get_google_access_token()
    if not access_token:
        return []

    params = {
        'access_token': access_token
    }
    url = 'https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}/values/promises'.format(
        spreadsheet_id=settings.GOOGLE_SPREADSHEET_ID)
    res = requests.get(url, params).json()

    if res.get('error') and res['error']['code'] == 401:
        # Reset access_token
        GoogleProfile.objects.all().delete()
        return []

    return res.get('values')


def get_google_access_token():
    gp = GoogleProfile.objects.first()
    return gp.credential.access_token if gp else None

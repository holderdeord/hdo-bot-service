import json
from django.conf import settings
from django.test import RequestFactory
from django.urls import reverse
from messenger_bot.views import webhook
from unittest import mock
from urllib.parse import urlencode


def test_webhook_get(rf: RequestFactory):
    query = {
        'hub.mode': 'subscribe',
        'hub.verify_token': settings.FACEBOOK_APP_VERIFICATION_TOKEN,
        'hub.challenge': 'this is a challenge'
    }
    request = rf.get("{}?{}".format(reverse('messenger_bot:webhook'), urlencode(query)))
    response = webhook(request)

    assert response.status_code == 200
    assert response.content.decode() == query['hub.challenge']


def test_webhook_post(rf: RequestFactory):
    data = {
        'object': 'page',
        'entry': [
            {
                'messaging': [
                    {
                        'recipient': {
                            'id': '1810488195865768'
                        },
                        'message': {
                            'sticker_id': 369239263222822,
                            'attachments': [
                                {
                                    'payload': {
                                        'sticker_id': 369239263222822,
                                        'url': 'https://scontent.xx.fbcdn.net/t39.1997-6/851557_369239266556155_759568595_n.png?_nc_ad=z-m'
                                    },
                                    'type': 'image'
                                }
                            ],
                            'mid': 'mid.1481651433417:0d504a6d80',
                            'seq': 15
                        },
                        'timestamp': 1481651433417,
                        'sender': {
                            'id': '1339474899459630'
                        }
                    }
                ],
                'time': 1481651540131,
                'id': '1810488195865768'
            }
        ]
    }
    request = rf.post(reverse('messenger_bot:webhook'), json.dumps(data), content_type='application/json')

    with mock.patch('requests.post') as external:
        external.return_value.ok = True
        response = webhook(request)
        assert external.call_count == 1, "Expecting exactly one response from the webhook"

        call_args = external.call_args_list[0]
        call_args_kwargs = call_args[1]

        assert 'json' in call_args_kwargs
        called_data = call_args_kwargs['json']

        assert called_data
        assert 'recipient' in called_data
        assert 'id' in called_data['recipient']
        assert '1339474899459630' == called_data['recipient']['id']

    assert response.status_code == 200

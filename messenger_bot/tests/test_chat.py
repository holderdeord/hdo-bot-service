import pytest
from django.core.management import call_command

from messenger_bot.chat import received_message


@pytest.mark.django_db()
def test_on_receive_messages():
    call_command('loaddata', 'testdata')
    incoming = {
        'sender': {
            'id': '1234'
        }
    }
    received_message(incoming)

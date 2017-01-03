import os
import pytest
from django.conf import settings
from django.core.management import call_command
from quiz.management.commands import sync_promises
from quiz.models import Promise


@pytest.mark.django_db
def test_sync_promises_command():
    test_data_external_id = 13020
    cmd = sync_promises.Command()
    call_command(cmd, os.path.join(settings.BASE_DIR, 'quiz/tests/testdata/check_file.csv'))
    assert Promise.objects.filter(external_id=test_data_external_id).count() == 1

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
    call_command(cmd, '--check-file', os.path.join(settings.BASE_DIR, 'quiz/tests/testdata/check_file.csv'))
    ps = Promise.objects.filter(external_id=test_data_external_id)
    assert ps.count() == 1
    p = ps.first()
    assert p.status == Promise.FULFILLED

    # Update data
    call_command(cmd, '--check-file', os.path.join(settings.BASE_DIR, 'quiz/tests/testdata/check_file_update.csv'))
    p.refresh_from_db()
    assert p.status == Promise.BROKEN

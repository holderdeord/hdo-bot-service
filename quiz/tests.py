import os

from django.conf import settings
from django.core.management import call_command
from django.test import TestCase

from quiz.management.commands import sync_promises
from quiz.models import Promise


class SyncPromises(TestCase):
    def test_sync_promises_command(self):
        test_data_external_id = 13020
        cmd = sync_promises.Command()
        call_command(cmd, os.path.join(settings.BASE_DIR, 'quiz/testdata/check_file.csv'))
        self.assertEqual(Promise.objects.filter(external_id=test_data_external_id).count(), 1)

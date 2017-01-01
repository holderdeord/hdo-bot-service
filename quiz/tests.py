import os

from django.conf import settings
from django.core.management import call_command
from django.test import TestCase

from quiz.management.commands import sync_promises


class SyncPromises(TestCase):
    def test_sync_promises_command(self):
        cmd = sync_promises.Command()
        call_command(cmd, os.path.join(settings.BASE_DIR, 'quiz/testdata/check_file.csv'))

import uuid
from django.db import models
from django.utils.translation import ugettext_lazy as _
from jsonfield import JSONField


class ChatSession(models.Model):
    STATE_IN_PROGRESS = 'in_progress'

    STATES = (
        (STATE_IN_PROGRESS, _('In progress')),
    )

    state = models.CharField(max_length=100, choices=STATES, default=STATE_IN_PROGRESS)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    user_id = models.CharField(max_length=100, db_index=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, db_index=True)
    meta = JSONField(blank=True)

    def __str__(self):
        return str(self.uuid.hex)

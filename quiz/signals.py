from django.db.models.signals import post_save
from django.dispatch import receiver

from messenger_bot.models import ChatSession
from quiz.models import Answer, AnswerSet


@receiver(post_save, sender=ChatSession, dispatch_uid='save-answers')
def save_answers(sender, instance: ChatSession, created, raw, **kwargs):
    """When a chat session is complete create answer objects (for statistical purposes)."""
    if raw:
        return

    if instance.state == ChatSession.STATE_COMPLETE:
        answer_data = instance.meta.get('answers')
        if not answer_data:
            return

        _as = AnswerSet.objects.create()
        for promise_id, state in answer_data.items():
            Answer.objects.create(promise_id=promise_id, status=state, session=instance, answer_set=_as)

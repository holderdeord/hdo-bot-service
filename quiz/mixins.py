from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.utils.translation import ugettext_lazy as _


class DefaultQuerySet(models.QuerySet):
    def get_default(self, default='default'):
        try:
            return self.get(default=default)
        except self.model.DoesNotExist:
            raise ImproperlyConfigured('At least one {} must have default={}'.format(self.model.__name__, default))
        except self.model.MultipleObjectsReturned:
            raise ImproperlyConfigured('Only one {} can have default={}'.format(self.model.__name__, default))


class DefaultMixin(models.Model):
    DEFAULT = 'default'
    DEFAULT_VOTER_GUIDE = 'default_vg'
    # DEFAULT_QUIZ = 'default_quiz'
    DEFAULT_NONE = 'none'

    DEFAULT_CHOICES = (
        (DEFAULT, _('Default')),
        (DEFAULT_VOTER_GUIDE, _('Voter guide')),
        # (DEFAULT_QUIZ, _('Quiz')),
        (DEFAULT_NONE, _('None')),
    )
    default = models.CharField(max_length=254, choices=DEFAULT_CHOICES, default=DEFAULT_NONE)

    def save(self, **kwargs):
        # Only one default per default type (except none)
        if self.default != self.DEFAULT_NONE:
            self.__class__.objects.filter(default=self.default).update(default=self.DEFAULT_NONE)
        super().save(**kwargs)

    objects = DefaultQuerySet.as_manager()

    class Meta:
        abstract = True

from django.core.exceptions import ImproperlyConfigured
from django.db import models


class IsDefaultQuerySet(models.QuerySet):
    def get_default(self):
        try:
            return self.get(is_default=True)
        except IsDefaultMixin.DoesNotExist:
            raise ImproperlyConfigured('At least one {} must have is_default set'.format(IsDefaultMixin.__name__))
        except IsDefaultMixin.MultipleObjectsReturned:
            raise ImproperlyConfigured('Only one {} can have is_default set'.format(IsDefaultMixin.__name__))


class IsDefaultMixin(models.Model):
    is_default = models.BooleanField(default=False)

    def save(self, **kwargs):
        # Only one default
        if self.is_default:
            self.__class__.objects.all().update(is_default=False)
        super().save(**kwargs)

    objects = IsDefaultQuerySet.as_manager()

    class Meta:
        abstract = True

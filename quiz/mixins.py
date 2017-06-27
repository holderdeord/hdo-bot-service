from django.core.exceptions import ImproperlyConfigured
from django.db import models


class IsDefaultMixin(models.Model):
    is_default = models.BooleanField(default=False)

    def save(self, **kwargs):
        # Only one default
        if self.is_default:
            self.__class__.objects.all().update(is_default=False)
        super().save(**kwargs)

    @classmethod
    def get_default(cls):
        try:
            return cls.objects.get(is_default=True)
        except cls.DoesNotExist:
            raise ImproperlyConfigured('At least one {} must have is_default set'.format(cls.__name__))
        except cls.MultipleObjectsReturned:
            raise ImproperlyConfigured('Only one {} can have is_default set'.format(cls.__name__))

    class Meta:
        abstract = True

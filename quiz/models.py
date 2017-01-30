from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Promise(BaseModel):
    """ We will do A"""
    FULFILLED = 'fulfilled'
    BROKEN = 'broken'
    NOT_YET_FULFILLED = 'not_yet'
    PARTIAL = 'partial'

    STATUS_CHOICES = (
        (FULFILLED, _('Fulfilled')),
        (BROKEN, _('Broken')),
        (NOT_YET_FULFILLED, _('Not Yet')),
        (PARTIAL, _('Partial')),
    )

    body = models.TextField()
    external_id = models.IntegerField(unique=True)
    promisor_name = models.CharField(max_length=255)
    parliament_period_name = models.CharField(max_length=255)
    source = models.CharField(max_length=255)
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, blank=True, default='')
    testable = models.BooleanField(default=True)

    parties = models.ManyToManyField('quiz.Party', blank=True, related_name='promises')
    categories = models.ManyToManyField('quiz.Category', blank=True, related_name='promises')

    def party_names(self):
        return self.parties.values_list('name', flat=True)

    def category_names(self):
        return self.categories.values_list('name', flat=True)

    def __str__(self):
        return self.body


class Interim(BaseModel):
    body = models.TextField()

    def __str__(self):
        return self.body


class Party(BaseModel):
    title = models.CharField(max_length=255)
    slug = models.SlugField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = _('Parties')


class Category(BaseModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name_plural = _('Categories')


class Manuscript(BaseModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class ManuscriptItem(BaseModel):
    manuscript = models.ForeignKey(Manuscript, on_delete=models.CASCADE, related_name='items')
    order = models.IntegerField()
    promise = models.ForeignKey(Promise, on_delete=models.CASCADE, null=True, blank=True)
    interim = models.ForeignKey(Interim, on_delete=models.CASCADE, null=True, blank=True)

    def clean(self):
        errors = {}
        fields = [self.promise, self.interim]

        if len([f for f in fields if f]) != 1:
            errors['foreign'] = 'Exactly one foreign key must be non-null'

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

#
# class Response(BaseModel):
#     # user response
#     pass
#
#
# class Session(BaseModel):
#     # Holds state of message session
#     pass

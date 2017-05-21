import uuid

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Count
from django.utils.translation import ugettext_lazy as _
from oauth2client.contrib.django_util.models import CredentialsField


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
        return '[{}] {}'.format(self.status, self.body)


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


class GoogleProfile(models.Model):
    """ For syncing promises from a Google Sheet """
    user = models.OneToOneField(User)
    credential = CredentialsField()


class Manuscript(BaseModel):
    name = models.CharField(max_length=255, blank=True, default='')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    promises = models.ManyToManyField(Promise, blank=True)
    # TODO: Text for boolean choices
    # TODO: type: generic, quiz or electoral_guide

    def __str__(self):
        return self.name if self.name else '#{}'.format(self.pk)


class ManuscriptImage(BaseModel):
    url = models.URLField()
    image = models.ImageField(null=True, blank=True)
    type = models.CharField(max_length=100, choices=Promise.STATUS_CHOICES, default=Promise.FULFILLED)

    def get_url(self):
        url = self.image.url if self.image else self.url

        return url if url else None


class ManuscriptItem(BaseModel):
    # TODO: random (til valgomaten) 3 og 3 opp til antall partier
    # TODO: electoral_guide (resultatet for valgomaten)
    TYPE_BUTTON = 'button'
    TYPE_PROMISES = 'promises'  # FIXME: replace with more generic question?
    TYPE_QUIZ_RESULT = 'quiz_result'
    TYPE_TEXT = 'text'
    TYPE_URL = 'url'

    TYPE_CHOICES = (
        (TYPE_BUTTON, _('Button')),
        (TYPE_PROMISES, _('Promises')),
        (TYPE_QUIZ_RESULT, _('Quiz results')),
        (TYPE_TEXT, _('Text')),
        (TYPE_URL, _('URL')),
    )

    type = models.CharField(max_length=100, choices=TYPE_CHOICES, default=TYPE_TEXT)
    manuscript = models.ForeignKey(Manuscript, on_delete=models.CASCADE, related_name='items')
    order = models.IntegerField(blank=True, default=0)
    text = models.TextField(blank=True, default='')
    button_text = models.TextField(blank=True, default='')
    url = models.URLField(blank=True, default='')

    class Meta:
        ordering = ('order',)

    def __str__(self):
        return 'ManuscriptItem<{}>'.format(self.pk)

    # TODO-maybe: support multiple buttons per item

    def save(self, *args, **kwargs):
        self._update_order()

        super().save(*args, **kwargs)

    def _update_order(self):
        if not self.order:
            _max = self.__class__.objects.filter().aggregate(models.Max('order'))
            try:
                self.order = _max['order'] + 1
            except TypeError:
                self.order = 0


class AnswerQuerySet(models.QuerySet):
    def correct_answers(self):
        return self.all().values('answers__correct_status').annotate(correct=Count('answers__correct_status')).order_by('correct')


class Answer(BaseModel):
    """ Simple model for saving responses """
    AGREE = 'agree'
    DISAGREE = 'disagree'
    ANSWER_CHOICES = (
        (AGREE, _('Agrees')),
        (DISAGREE, _('Diagrees')),
    )
    promise = models.ForeignKey('quiz.Promise')
    status = models.CharField(max_length=255, choices=Promise.STATUS_CHOICES, blank=True, default='',
                              help_text=_('Used with kept/broken quiz'))
    answer = models.CharField(max_length=255, choices=ANSWER_CHOICES, blank=True, default='',
                              help_text=_('Used with voting guide'))
    correct_status = models.BooleanField(default=False, blank=True)

    answer_set = models.ForeignKey('quiz.AnswerSet', null=True, blank=True, related_name='answers')


class AnswerSet(BaseModel):
    session = models.OneToOneField(
        'messenger_bot.ChatSession', null=True, blank=True, related_name='answers', on_delete=models.SET_NULL)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)

    objects = AnswerQuerySet.as_manager()


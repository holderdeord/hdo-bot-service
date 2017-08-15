import uuid

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Count
from django.utils.translation import ugettext_lazy as _
from oauth2client.contrib.django_util.models import CredentialsField

from quiz.mixins import DefaultMixin


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class PromiseReference(BaseModel):
    url = models.URLField()
    title = models.CharField(max_length=255)

    promise = models.ForeignKey('quiz.Promise', on_delete=models.CASCADE, related_name='references')


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
    description = models.TextField(default='')

    parties = models.ManyToManyField('quiz.Party', blank=True, related_name='promises')
    categories = models.ManyToManyField('quiz.Category', blank=True, related_name='promises')
    hdo_categories = models.ManyToManyField('quiz.HdoCategory', blank=True, related_name='promises')

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


class ManuscriptImage(BaseModel):
    url = models.URLField()
    image = models.ImageField(null=True, blank=True)
    type = models.CharField(max_length=100, choices=Promise.STATUS_CHOICES, default=Promise.FULFILLED)

    def get_url(self):
        url = self.image.url if self.image else self.url

        return url if url else None


class Manuscript(DefaultMixin, BaseModel):
    """ A group/collection of ManuscriptItems """
    TYPE_QUIZ = 'quiz'
    TYPE_VOTER_GUIDE = 'voter_guide'
    TYPE_GENERIC = 'generic'

    TYPE_CHOICES = (
        (TYPE_GENERIC, _('Generic')),
        (TYPE_QUIZ, _('Quiz')),
        (TYPE_VOTER_GUIDE, _('Voter guide')),
    )

    name = models.CharField(
        max_length=255,
        blank=True,
        default='',
        help_text=_('Used both for admin display and user display when type=voting guide'),
        unique=True)
    type = models.CharField(max_length=100, choices=TYPE_CHOICES, default=TYPE_GENERIC)
    category = models.ForeignKey('quiz.Category', on_delete=models.SET_NULL, blank=True, null=True)
    promises = models.ManyToManyField('quiz.Promise', blank=True)

    next = models.ForeignKey('self', related_name='prev', blank=True, null=True)

    hdo_category = models.ForeignKey(
        'quiz.HdoCategory', on_delete=models.SET_NULL, blank=True, null=True, related_name='manuscripts')
    is_first_in_category = models.BooleanField(
        default=False,
        blank=True,
        help_text=_('Which manuscript in a category comes first (used with TYPE_VG_CATEGORY_SELECT)'))

    def __str__(self):
        return '{} ({})'.format(self.name, self.type) if self.name else '#{}'.format(self.pk)


class VoterGuideAlternative(BaseModel):
    """Tema, tekst, løfte-ider"""
    text = models.CharField(max_length=255)
    manuscript = models.ForeignKey('quiz.Manuscript', related_name='voter_guide_alternatives')
    promises = models.ManyToManyField('quiz.Promise', blank=True)
    no_answer = models.BooleanField(default=False, blank=True)

    class Meta:
        unique_together = ('text', 'manuscript')

    def set_text(self, text):
        self.text = text

    def __str__(self):
        return self.text


class ManuscriptItem(BaseModel):
    """ A block, ordered

        Note: Types are pretty specific for our task.
        Could be made generic in the future with inspiration from chatfuel.com interface
    """

    # Generic blocks
    TYPE_TEXT = 'text'
    TYPE_QUICK_REPLY = 'quick_reply'
    TYPE_URL = 'url'

    # Quiz
    TYPE_QUIZ_RESULT = 'quiz_result'
    TYPE_Q_PROMISES_CHECKED = 'quiz_q_promises_checked'
    TYPE_Q_PARTY_SELECT = 'quiz_q_party_select'
    TYPE_Q_PARTY_BOOL = 'quiz_q_party_bool'

    # Voter guide
    TYPE_VG_RESULT = 'vg_result'  # Show preliminary results
    TYPE_VG_CATEGORY_SELECT = 'vg_categories'  # Show category select
    TYPE_VG_QUESTIONS = 'vg_questions'  # List promises in text w/ quick reply per party

    QUICK_REPLY_TEXT_FIELDS = ['reply_text_1', 'reply_text_2', 'reply_text_3']
    QUICK_REPLY_ACTION_FIELDS = ['reply_action_1', 'reply_action_2', 'reply_action_3']
    QUICK_REPLY_FIELDS = dict(zip(QUICK_REPLY_TEXT_FIELDS, QUICK_REPLY_ACTION_FIELDS))

    TYPE_CHOICES = (
        (TYPE_TEXT, _('Text')),
        (TYPE_QUICK_REPLY, _('Quick reply')),
        (TYPE_URL, _('URL')),
        (TYPE_QUIZ_RESULT, _('Quiz: Show result')),
        (TYPE_Q_PROMISES_CHECKED, _('Quiz: Show checked promise questions')),
        (TYPE_Q_PARTY_SELECT, _('Quiz: Show which party promised what questions')),
        (TYPE_Q_PARTY_BOOL, _('Quiz: Show did party x promise y questions')),
        (TYPE_VG_RESULT, _('Voter guide: Show result')),
        (TYPE_VG_CATEGORY_SELECT, _('Voter guide: Show category select')),
        (TYPE_VG_QUESTIONS, _('Voter guide: Show questions')),
    )

    type = models.CharField(max_length=100, choices=TYPE_CHOICES, default=TYPE_TEXT)
    manuscript = models.ForeignKey('quiz.Manuscript', on_delete=models.CASCADE, related_name='items')
    order = models.IntegerField(blank=True, default=0)
    text = models.TextField(blank=True, default='')
    url = models.URLField(blank=True, default='')

    # FIXME: Classic "get's the job done"-code incoming
    reply_text_1 = models.TextField(blank=True, default='')
    reply_text_2 = models.TextField(blank=True, default='')
    reply_text_3 = models.TextField(blank=True, default='')
    reply_action_1 = models.ForeignKey('quiz.Manuscript', related_name='action_1_items', blank=True, null=True)
    reply_action_2 = models.ForeignKey('quiz.Manuscript', related_name='action_2_items', blank=True, null=True)
    reply_action_3 = models.ForeignKey('quiz.Manuscript', related_name='action_3_items', blank=True, null=True)

    class Meta:
        ordering = ('order',)

    def __str__(self):
        return 'ManuscriptItem<{}>'.format(self.pk)

    def save(self, *args, **kwargs):
        self._update_order()

        super().save(*args, **kwargs)

    def _update_order(self):
        if not self.order:
            _max = self.__class__.objects.filter().aggregate(order=models.Max('order'))
            try:
                self.order = _max['order'] + 1
            except TypeError:
                self.order = 0


class AnswerQuerySet(models.QuerySet):
    def correct_answers(self):
        qs = self.all().values('answers__correct_status').annotate(correct=Count('answers__correct_status'))
        return qs.order_by('correct')


class Answer(BaseModel):
    """ Simple model for saving responses """
    AGREE = 'agree'
    DISAGREE = 'disagree'
    ANSWER_CHOICES = (
        (AGREE, _('Agrees')),
        (DISAGREE, _('Disagrees')),
    )
    promise = models.ForeignKey('quiz.Promise')
    status = models.CharField(max_length=255, choices=Promise.STATUS_CHOICES, blank=True, default='',
                              help_text=_('Used with kept/broken quiz'))
    answer = models.CharField(max_length=255, choices=ANSWER_CHOICES, blank=True, default='',
                              help_text=_('Used with voting guide'))
    correct_status = models.BooleanField(default=False, blank=True)

    answer_set = models.ForeignKey(
        'quiz.AnswerSet', null=True, blank=True, related_name='answers', on_delete=models.CASCADE)

    def __str__(self):
        return '{}: {}'.format(self.__class__.__name__, self.pk)


class VoterGuideAnswer(BaseModel):
    """ Voting guide responses """
    voter_guide_alternative = models.ForeignKey(
        'quiz.VoterGuideAlternative', null=True, on_delete=models.SET_NULL, related_name='answers')
    answer_set = models.ForeignKey(
        'quiz.AnswerSet', null=True, blank=True, related_name='voter_guide_answers', on_delete=models.CASCADE)

    def __str__(self):
        return '{}: {}'.format(self.__class__.__name__, self.pk)


class AnswerSet(BaseModel):
    session = models.OneToOneField(
        'messenger.ChatSession', null=True, blank=True, related_name='answers', on_delete=models.SET_NULL)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)

    objects = AnswerQuerySet.as_manager()

    def __str__(self):
        return '{}: {}'.format(self.__class__.__name__, self.pk)


class HdoCategory(BaseModel):
    name = models.CharField(max_length=255)
    label = models.CharField(max_length=255, blank=True, default='', help_text=_('Quick reply labels'))

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name_plural = _('HDO Categories')

import csv
import logging

from django.core.management import BaseCommand

from quiz.models import Manuscript, ManuscriptItem, QuizAlternative
from quiz.utils import PARTY_SHORT_NAME_SLUGS

logger = logging.getLogger(__name__)

PARTY_SHORT_TO_LONG = {v: k for k, v in PARTY_SHORT_NAME_SLUGS.items()}


class Command(BaseCommand):
    """
    Import manuscripts from general quiz sheet
    """

    def add_arguments(self, parser):
        parser.add_argument('file', type=str, help='Import manuscripts from file')

    def handle(self, *args, **options):
        manuscripts_data = self.get_manuscript_data(options['file'])

        for m in manuscripts_data:
            has_correct = False
            for a in m['alternatives']:
                if m['correct_alternative'] == a['number']:
                    has_correct = True

            if not has_correct:
                raise Exception(
                    "Oops, inconsistent data! Manuscript {} does not have an alternative marked as correct".format(
                        m['name']))

        first_manuscript = self.create_manuscripts(manuscripts_data)
        self.create_start_manuscript(first_manuscript)

    def get_manuscript_data(self, file_path):
        """ One manuscript per line """
        manuscripts = []
        alt_columns = ['Alternativ {}'.format(i) for i in range(1, 4)]
        typemap = {
            'Party': ManuscriptItem.TYPE_Q_PARTY_QUESTION,
            'Text': ManuscriptItem.TYPE_GQ_QUESTION,
            'Yes or no': ManuscriptItem.TYPE_GQ_YES_OR_NO_QUESTION,

        }

        with open(file_path) as f:
            csv_file = csv.DictReader(f)
            for row in csv_file:
                correct_alternative = int(row['Riktig alternativ'])
                manuscript_name = row['Spørsmål']
                question_type = typemap[row['Spørsmålstype']]

                alternatives = []
                for col in alt_columns:
                    alt = row[col]

                    if len(alt.strip()) == 0:
                        continue

                    if question_type == ManuscriptItem.TYPE_Q_PARTY_QUESTION:
                        alt = PARTY_SHORT_TO_LONG[alt.lower()]
                    alternatives.append({
                        'text': alt,
                        'number': int(col[-1])
                    })

                manuscripts.append({
                    'name': manuscript_name,
                    'alternatives': alternatives,
                    'correct_alternative': correct_alternative,
                    'manuscript_item_type': question_type
                })

        return manuscripts

    def create_start_manuscript(self, start):
        # Quiz
        manuscript, created = Manuscript.objects.get_or_create(
            name='Quiz start',
            default=Manuscript.DEFAULT_QUIZ)

        if created:
            ManuscriptItem.objects.get_or_create(
                type=ManuscriptItem.TYPE_QUICK_REPLY,
                manuscript=manuscript,
                order=1,
                text='Start quiz',
                reply_text_1='Start quiz',
                reply_action_1=start)

    def create_manuscripts(self, manuscripts_data):
        first = None
        for m in manuscripts_data:
            correct_alternative = m.pop('correct_alternative')
            manuscript_item_type = m.pop('manuscript_item_type')
            alts = m.pop('alternatives')

            m = Manuscript.objects.create(type=Manuscript.TYPE_QUIZ, **m)
            m.save()

            if first is None:
                first = m

            for a in alts:
                q = QuizAlternative.objects.create(
                    text=a['text'],
                    correct_answer=correct_alternative == a['number'],
                    manuscript=m)

                q.save()

            ManuscriptItem.objects.get_or_create(
                type=manuscript_item_type,
                manuscript=m,
                order=1)

        return first

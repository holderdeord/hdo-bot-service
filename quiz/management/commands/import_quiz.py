import csv
import logging
from collections import defaultdict
from pprint import pprint

import re
from django.core.management import BaseCommand

from quiz.models import Manuscript, HdoCategory, Promise, ManuscriptItem, QuizAlternative
from quiz.utils import PARTY_SHORT_NAMES, PARTY_SHORT_NAME_SLUGS

logger = logging.getLogger(__name__)

PARTY_SHORT_TO_LONG = {v: k for k, v in PARTY_SHORT_NAME_SLUGS.items()}
LEVEL_MAP = {
    'Lav': Manuscript.LEVEL_LOW,
    'Middels': Manuscript.LEVEL_MEDIUM,
    'Høy': Manuscript.LEVEL_HIGH,
}
REPLACE_SYMBOL = '___'


class Command(BaseCommand):
    """
    Import manuscripts from quiz sheet

    Ref: https://data.holderdeord.no/api/promises/

    """

    def add_arguments(self, parser):
        parser.add_argument('--category-map', type=str, default='./file/category_map.csv',
                            help='Path to file with mapping between categories and HDO categories')
        parser.add_argument('file', type=str, help='Import manuscripts from file')

    def handle(self, *args, **options):
        self.init_categories()
        self.create_start_manuscript()
        manuscripts_data = self.get_manuscript_data(options['file'])
        self.create_manuscripts(manuscripts_data)

    @staticmethod
    def _clean_parties(parties, promises):
        ps = []
        for p in parties:
            p = p.lower()
            ps.append({
                'text': PARTY_SHORT_TO_LONG[p],
                'promises': promises.get(p, [])
            })

            if p.lower() not in PARTY_SHORT_NAME_SLUGS.values():
                raise Exception('Oops \'{}\' not a party'.format(p))

        return ps

    @staticmethod
    def _clean_promise(promise):
        parties = []
        for p in PARTY_SHORT_NAMES.values():
            if p == 'V':
                p = 'Venstre'
            elif p == 'H':
                p = 'Høyre'

            parties.append(p)

        party_strip_re = re.compile('|'.join(parties))
        return party_strip_re.sub(REPLACE_SYMBOL, promise)

    def get_manuscript_data(self, file_path):
        """ One manuscript per line """
        manuscripts = []
        strip_re = re.compile(r'\s+')

        with open(file_path) as f:
            csv_file = csv.DictReader(f)
            for row in csv_file:
                if row['Løfte-ID'] == '':
                    continue

                hdo_category = row['HDO-kategori']
                level = LEVEL_MAP[row['Nivå (Lav/Middels/Høy)']]
                party_alternatives = row['Partier'].split('/')
                correct_promise = int(row['Løfte-ID'])
                manuscript_name = row['Løfte-tekst']

                party_promises = defaultdict(list)
                for party in PARTY_SHORT_NAMES.values():
                    v = row[party]
                    if v:
                        v = strip_re.sub('', v).split('/')
                        v = map(int, v)
                        party_promises[party.lower()] += v

                manuscripts.append({
                    'name': self._clean_promise(manuscript_name),
                    'hdo_category': self.cat_map[hdo_category],
                    'level': level,
                    'alternatives': self._clean_parties(party_alternatives, party_promises),
                    'party_promises': list([item for sublist in party_promises.values() for item in sublist]),
                    'correct_promise': correct_promise,
                })

        return manuscripts

    def create_start_manuscript(self):
        # Quiz
        manuscript, created = Manuscript.objects.get_or_create(
            name='Quiz start',
            default=Manuscript.DEFAULT_QUIZ)

        if created:
            ManuscriptItem.objects.get_or_create(
                type=ManuscriptItem.TYPE_Q_CATEGORY_SELECT,
                manuscript=manuscript,
                order=1,
                text='Velg tema')

    def create_manuscripts(self, manuscripts_data):
        for m in manuscripts_data:
            pprint(m)
            promises = Promise.objects.filter(pk__in=m.pop('party_promises'))
            correct_promise = m.pop('correct_promise')
            alts = m.pop('alternatives')

            m = Manuscript.objects.create(type=Manuscript.TYPE_QUIZ, **m)
            m.promises = promises
            m.save()

            for a in alts:
                q = QuizAlternative.objects.create(
                    text=a['text'],
                    correct_answer=correct_promise in a['promises'],
                    manuscript=m)

                q.promises = Promise.objects.filter(pk__in=a['promises'])
                q.save()

            ManuscriptItem.objects.get_or_create(
                type=ManuscriptItem.TYPE_Q_QUESTION,
                manuscript=m,
                order=1)

    def init_categories(self):
        cats = [
            'Arbeid og sosial',
            'Familie og likestilling',
            'Helse og omsorg',
            'Innvandring og asyl',
            'Justis og beredskap',
            'Klima, energi og miljø',
            'Kultur, religion og frivillighet',
            'Landbruk og fiskeri',
            'Offentlig forvaltning',
            'Økonomi og næringsliv',
            'Transport og kommunikasjon',
            'Utdanning og forskning',
            'Utenriks og forsvar',
        ]
        for c in cats:
            HdoCategory.objects.get_or_create(name=c)

        self.cat_map = dict({cat.name: cat for cat in HdoCategory.objects.all()})

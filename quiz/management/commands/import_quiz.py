import csv
import logging
from pprint import pprint

from django.core.management import BaseCommand
from django.utils.translation import ugettext_lazy as _

from quiz.models import Manuscript, HdoCategory, VoterGuideAlternative, Promise, ManuscriptItem
from quiz.utils import PARTY_SHORT_NAMES, PARTY_SHORT_NAME_SLUGS

logger = logging.getLogger(__name__)


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
        manuscripts_data = self.get_manuscript_data(options['file'])
        pprint(manuscripts_data)

    def get_manuscript_data(self, file_path):
        """ One manuscript per line """
        manuscripts = []

        with open(file_path) as f:
            csv_file = csv.DictReader(f)
            for row in csv_file:
                if row['Løfte-ID'] == '':
                    continue

                manuscript_name = row['Løfte-tekst']
                hdo_category = row['HDO-kategori']
                level = row['Nivå (Lav/Middels/Høy)']

                party_alternatives = []
                # TODO: You are here

                manuscripts.append({
                    'name': manuscript_name,
                    'hdo_category': hdo_category,
                    'level': level,
                    'alternatives': []
                })

        return manuscripts

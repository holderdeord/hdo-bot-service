import csv
import logging
from django.core.management import BaseCommand

from quiz.models import Manuscript, HdoCategory, VoterGuideAlternative, Promise


class Command(BaseCommand):
    """
    Import manuscripts from electoral guide

    Ref: https://data.holderdeord.no/api/promises/

    """

    def add_arguments(self, parser):
        parser.add_argument('--category-map', type=str,
                            help='Path to file with mapping between categories and HDO categories')
        parser.add_argument('--file', type=str,
                            help='Import manuscripts from file')

    def handle(self, *args, **options):
        # logging.info('test', options['category_map'], options['file'])
        manuscripts = self.get_manuscripts(options['file'])
        for manuscript_name in manuscripts:
            hdo_category = self.get_hdo_category(manuscripts[manuscript_name]['hdo_category'])
            manuscript, created = Manuscript.objects.get_or_create(
                name=manuscript_name,
                type='voter_guide',
                hdo_category=hdo_category
            )
            for alternative_data in manuscripts[manuscript_name]['alternatives']:
                alternative, created = VoterGuideAlternative.objects.get_or_create(
                    text=alternative_data['text'],
                    manuscript=manuscript
                )
                alternative.save()
                promises = list(map(self.get_promise, alternative_data['promises']))
                alternative.promises.add(*promises)
                alternative.save()

    def get_manuscripts(self, file_path):
        manuscripts = {}
        with open(file_path) as f:
            csv_file = csv.DictReader(f)
            for row in csv_file:
                if row['Løfte-ID'] == '':
                    continue
                manuscript_name = row['Tema']
                if manuscript_name in manuscripts:
                    manuscripts[manuscript_name]['alternatives'].append(self.create_alternative(row))
                else:
                    manuscripts[manuscript_name] = {
                        'hdo_category': row['HDO-kategori'],
                        'manuscript_name': row['Tema'],
                        'alternatives': [self.create_alternative(row)]
                    }
        return manuscripts

    def create_alternative(self, row):
        def strip_promise(promise):
            return promise.strip()

        return {
            'text': row['Tekst'],
            'promises': list(map(strip_promise, row['Løfte-ID'].split('/')))
        }

    def get_hdo_category(self, hdo_category_name):
        return HdoCategory.objects.get_or_create(name=hdo_category_name)[0]

    def get_promise(self, external_id):
        return Promise.objects.get(external_id=external_id)

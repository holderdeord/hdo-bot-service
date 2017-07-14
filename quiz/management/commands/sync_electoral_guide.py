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
        manuscripts_data = self.get_manuscripts_data(options['file'])
        manuscripts = self.add_manuscripts_to_db(manuscripts_data)
        root_manuscript = Manuscript.objects.get_or_create(name='Valgomat start')
        hdo_categories = self.group_into_hdo_categories(manuscripts)
        for hdo_category in hdo_categories:
            self.link_manuscripts(hdo_category, root_manuscript)
            # logging.info(hdo_categories)

    def add_manuscripts_to_db(self, manuscripts_data):
        manuscripts = {}
        for manuscript_data in manuscripts_data:
            hdo_category = self.get_hdo_category(manuscript_data['hdo_category'])
            manuscript, created = Manuscript.objects.get_or_create(
                name=manuscript_data['name'],
                type='voter_guide',
                hdo_category=hdo_category
            )
            manuscripts[manuscript.pk] = manuscript
            for alternative_data in manuscript_data['alternatives']:
                alternative, created = VoterGuideAlternative.objects.get_or_create(
                    text=alternative_data['text'],
                    manuscript=manuscript
                )
                alternative.save()
                promises = list(map(self.get_promise, alternative_data['promises']))
                alternative.promises.add(*promises)
                alternative.save()
        return [v for v in manuscripts.values()]

    def get_manuscripts_data(self, file_path):
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
                        'name': manuscript_name,
                        'hdo_category': row['HDO-kategori'],
                        'manuscript_name': row['Tema'],
                        'alternatives': [self.create_alternative(row)]
                    }
        return [v for v in manuscripts.values()]

    def find_linked_manuscripts(self, hdo_category):
        linked_manuscripts = []
        unlinked_manuscripts = []
        for manuscript in hdo_category['manuscripts']:
            if manuscript.items.count() > 0:
                linked_manuscripts.append(manuscript)
            else:
                unlinked_manuscripts.append(manuscript)
        return linked_manuscripts, unlinked_manuscripts

    def group_into_hdo_categories(self, manuscripts):
        hdo_categories = {}
        for manuscript in manuscripts:
            hdo_category_pk = manuscript.hdo_category.pk
            if hdo_category_pk in hdo_categories:
                hdo_categories[hdo_category_pk]['manuscripts'].append(manuscript)
            else:
                hdo_categories[hdo_category_pk] = {
                    'category': manuscript.hdo_category,
                    'manuscripts': [manuscript]
                }
        return [v for v in hdo_categories.values()]

    def link_manuscripts(self, hdo_category, root_manuscript):
        linked_manuscripts, unlinked_manuscripts = self.find_linked_manuscripts(hdo_category)
        number_of_unlinked_manuscripts = len(unlinked_manuscripts)
        for index, manuscript in enumerate(unlinked_manuscripts):
            if index + 1 < number_of_unlinked_manuscripts:
                self.createManuscriptItemThatLinks(manuscript, unlinked_manuscripts[index + 1])
            elif len(linked_manuscripts) > 0:
                logging.info('continue adding')
            else:
                logging.info('end stuff')

    def createManuscriptItemThatLinks(self, current_manuscript, next_manuscript):

        logging.info('link stuff')

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

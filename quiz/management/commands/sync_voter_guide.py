import csv
import logging

from django.core.management import BaseCommand
from django.utils.translation import ugettext_lazy as _

from quiz.models import Manuscript, HdoCategory, VoterGuideAlternative, Promise, ManuscriptItem
from quiz.utils import PARTY_SHORT_NAMES


class Command(BaseCommand):
    """
    Import manuscripts from electoral guide

    Ref: https://data.holderdeord.no/api/promises/

    """

    DO_NOT_KNOW = 'do_not_know'

    TEXTS = (
        (DO_NOT_KNOW, _('Vet ikke'))
    )

    def add_arguments(self, parser):
        parser.add_argument('--category-map', type=str, default='./file/category_map.csv',
                            help='Path to file with mapping between categories and HDO categories')
        parser.add_argument('file', type=str,
                            help='Import manuscripts from file', )

    def handle(self, *args, **options):
        manuscripts_data_list = self.get_manuscripts_data(options['file'])
        self.create_question_manuscripts(manuscripts_data_list)
        self.create_vg_start_manuscript()

    def get_manuscripts_data(self, file_path):
        manuscripts = {}
        with open(file_path) as f:
            csv_file = csv.DictReader(f)
            for row in csv_file:
                if row['Løfte-ID'] == '':
                    continue
                manuscript_name = row['Spørsmål']
                hdo_category = row['Tema (HDO-kategori)']
                question_text = row['Spørsmålstekst']
                if manuscript_name in manuscripts:
                    manuscripts[manuscript_name]['alternatives'].append(self.create_alternative(row))
                else:
                    manuscripts[manuscript_name] = {
                        'name': manuscript_name,
                        'hdo_category': hdo_category,
                        'question_text': question_text,
                        'alternatives': [self.create_alternative(row)]
                    }
        return [v for v in manuscripts.values()]

    def create_question_manuscripts(self, manuscripts_data_list):
        manuscripts = {}
        logging.info('Tema (HDO-kategori),Spørsmål,Spørsmålstekst,Partier')
        for manuscript_data in manuscripts_data_list:
            hdo_category = self.get_hdo_category(manuscript_data['hdo_category'])
            vg_manuscript, created = Manuscript.objects.get_or_create(
                name=manuscript_data['name'],
                type=Manuscript.TYPE_VOTER_GUIDE,
                hdo_category=hdo_category
            )
            ManuscriptItem.objects.get_or_create(
                type=ManuscriptItem.TYPE_TEXT,
                manuscript=vg_manuscript,
                order=1,
                text=manuscript_data['question_text']
            )
            manuscripts[vg_manuscript.pk] = vg_manuscript
            parties_known = []
            for alternative_data in manuscript_data['alternatives']:
                alternative, created = VoterGuideAlternative.objects.get_or_create(
                    text=alternative_data['text'],
                    manuscript=vg_manuscript
                )
                alternative.save()
                promise_ids = list(map(self.get_promise_id, alternative_data['promises']))
                alternative.promises.add(*promise_ids)
                alternative.save()

                parties = self.get_parties_for_alternative(alternative)
                parties_known += parties
                alternative.text = self.get_alt_text(alternative_data, parties)
                alternative.save()

            parties_unknown = [x for x in PARTY_SHORT_NAMES.values() if x not in set(parties_known)]
            logging.info('"{}","{}","{}","{}"'.format(
                hdo_category,
                manuscript_data['name'],
                manuscript_data['question_text'],
                ', '.join(sorted(parties_unknown))
            ))
            self.create_do_not_know_alternative(vg_manuscript, parties_unknown)
            self.create_starting_manuscript_item(vg_manuscript)
        return [v for v in manuscripts.values()]

    def get_alt_text(self, alternative_data, parties, with_parties=False):
        parties_txt = ''
        if with_parties:
            parties_txt = ' ({})'.format(', '.join(sorted(set(parties))))

        return '{}{}'.format(alternative_data['text'], parties_txt)

    def create_vg_start_manuscript(self):
        manuscript, created = Manuscript.objects.get_or_create(
            name='Valgomat start',
            default=Manuscript.DEFAULT_VOTER_GUIDE
        )
        if created:
            ManuscriptItem.objects.get_or_create(
                type=ManuscriptItem.TYPE_VG_CATEGORY_SELECT,
                manuscript=manuscript,
                order=1,
                text='Velg tema',
            )

    def create_do_not_know_alternative(self, manuscript, parties_unknown, with_parties=False):
        formatted = ''
        if with_parties and parties_unknown:
            formatted = ' ({})'.format(', '.join(parties_unknown))
        VoterGuideAlternative.objects.get_or_create(
            text='Vet ikke{}'.format(formatted),
            manuscript=manuscript,
            no_answer=True)

    def find_linked_manuscripts(self, hdo_category):
        linked_manuscripts = []
        unlinked_manuscripts = []
        for manuscript in hdo_category['manuscripts']:
            if manuscript.items.count() > 1:
                linked_manuscripts.append(manuscript)
            else:
                unlinked_manuscripts.append(manuscript)
        return linked_manuscripts, unlinked_manuscripts

    def create_starting_manuscript_item(self, manuscript):
        ManuscriptItem.objects.get_or_create(
            type=ManuscriptItem.TYPE_VG_QUESTIONS,
            manuscript=manuscript,
            order=1,
        )

    def create_alternative(self, row):
        def strip_promise(promise):
            return promise.strip()

        return {
            'text': row['Tekst'],
            'promises': list(map(strip_promise, row['Løfte-ID'].split('/')))
        }

    def get_hdo_category(self, hdo_category_name):
        return HdoCategory.objects.get_or_create(name=hdo_category_name)[0]

    def get_promise_id(self, external_id):
        return Promise.objects.get(external_id=external_id)

    def get_parties_for_alternative(self, alternative):
        promisors = alternative.promises.values_list('promisor_name', flat=True)
        return [PARTY_SHORT_NAMES[party] for party in promisors]

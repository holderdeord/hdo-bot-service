import csv
import logging

from django.core.management import BaseCommand
from django.utils.translation import ugettext_lazy as _

from quiz.models import Manuscript, HdoCategory, VoterGuideAlternative, Promise, ManuscriptItem


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
        vg_start_manuscript = self.create_vg_start_manuscript()
        self.create_root_manuscript(vg_start_manuscript)

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
            for alternative_data in manuscript_data['alternatives']:
                alternative, created = VoterGuideAlternative.objects.get_or_create(
                    text=alternative_data['text'],
                    manuscript=vg_manuscript
                )
                alternative.save()
                promise_ids = list(map(self.get_promise_id, alternative_data['promises']))
                alternative.promises.add(*promise_ids)
                alternative.save()
                parties = ', '.join(self.get_parties_for_alternative(alternative))
                alternative.set_text('{} ({})'.format(alternative_data['text'], parties))
                alternative.save()
            self.create_do_not_know_alternative(vg_manuscript)
            self.create_starting_manuscript_item(vg_manuscript)
        return [v for v in manuscripts.values()]

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
                text='Velg et tema som du bryr deg om',
            )
        return manuscript

    def create_root_manuscript(self, vg_start_manuscript):
        manuscript, created = Manuscript.objects.get_or_create(
            name='Chatbort start',
            default=Manuscript.DEFAULT,
            next=vg_start_manuscript
        )
        if created:
            ManuscriptItem.objects.get_or_create(
                type=ManuscriptItem.TYPE_QUICK_REPLY,
                manuscript=manuscript,
                order=1,
                text="Finn din politiske match! Svar på minst åtte spørsmål, og finn ut hvem du burde heie på ved valget.",
                reply_text_1="Jeg er klar!",
                reply_action_1=vg_start_manuscript
            )
        return manuscript

    def create_do_not_know_alternative(self, manuscript):
        VoterGuideAlternative.objects.get_or_create(
            text='Vet ikke',
            manuscript=manuscript
        )

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
        def get_party_name(promise):
            return promise.promisor_name[:3]

        promises = alternative.promises.all()
        return set(list(map(get_party_name, promises)))

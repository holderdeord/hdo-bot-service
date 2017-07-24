import csv
import logging
from django.core.management import BaseCommand
from django.db import connection

from quiz.models import Manuscript, HdoCategory, VoterGuideAlternative, Promise, ManuscriptItem


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
        manuscripts_data = self.get_manuscripts_data(options['file'])
        manuscripts = self.add_manuscripts_to_db(manuscripts_data)
        root_manuscript = self.create_root_manuscript()
        hdo_categories = self.group_into_hdo_categories(manuscripts)
        for hdo_category in hdo_categories:
            self.link_manuscripts(hdo_category, root_manuscript)

    def add_manuscripts_to_db(self, manuscripts_data):
        manuscripts = {}
        for manuscript_data in manuscripts_data:
            hdo_category = self.get_hdo_category(manuscript_data['hdo_category'])
            manuscript, created = Manuscript.objects.get_or_create(
                name=manuscript_data['name'],
                type=Manuscript.TYPE_VOTER_GUIDE,
                hdo_category=hdo_category
            )
            manuscripts[manuscript.pk] = manuscript
            if created:
                for alternative_data in manuscript_data['alternatives']:
                    alternative, created = VoterGuideAlternative.objects.get_or_create(
                        text=alternative_data['text'],
                        manuscript=manuscript
                    )
                    alternative.save()
                    promises = list(map(self.get_promise, alternative_data['promises']))
                    alternative.promises.add(*promises)
                    alternative.save()
                self.create_starting_manuscript_item(manuscript)
        return [v for v in manuscripts.values()]

    def create_root_manuscript(self):
        manuscript, created = Manuscript.objects.get_or_create(
            name='Valgomat start',
            is_default=True
        )
        if created:
            ManuscriptItem.objects.get_or_create(
                type='vg_categories',
                manuscript=manuscript,
                text='Velg den kategorien du syns er mest interessant.'
            )
        return manuscript

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
            if manuscript.items.count() > 1:
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
        number_of_linked_manuscripts = len(linked_manuscripts)
        number_of_unlinked_manuscripts = len(unlinked_manuscripts)

        # link unlinked manuscripts
        for index, manuscript in enumerate(unlinked_manuscripts):
            if index + 1 < number_of_unlinked_manuscripts:
                next_manuscript = unlinked_manuscripts[index + 1]
                manuscript.next = next_manuscript
                self.create_manuscript_item_that_links_to_next_manuscript(manuscript, next_manuscript)
            else:
                manuscript.next = root_manuscript
                self.create_manuscript_item_that_links_to_root_manuscript(manuscript, root_manuscript)
            manuscript.save()

        # link newly linked manuscripts to previously linked manuscripts
        if number_of_linked_manuscripts > 0 and number_of_unlinked_manuscripts > 0:
            last_manuscript = next(x for x in linked_manuscripts if x.next == root_manuscript)
            first_manuscript = unlinked_manuscripts[0]
            # remove current items
            last_manuscript.items.all().delete()
            # add new items
            self.create_starting_manuscript_item(last_manuscript)
            self.create_manuscript_item_that_links_to_next_manuscript(last_manuscript, first_manuscript)
            # update next
            last_manuscript.next = first_manuscript
            last_manuscript.save()

        # set is_first_in_category on first manuscript, if necessary
        if number_of_linked_manuscripts == 0:
            unlinked_manuscripts[0].is_first_in_category = True
            unlinked_manuscripts[0].save()

    def create_starting_manuscript_item(self, manuscript):
        ManuscriptItem.objects.get_or_create(
            type=ManuscriptItem.TYPE_VG_QUESTIONS,
            manuscript=manuscript,
            order=1,
            text='Temaet er {}, hvilken påstand er du mest enig i?'.format(manuscript.name)
        )

    def create_manuscript_item_that_links_to_root_manuscript(self, current_manuscript, root_manuscript):
        ManuscriptItem.objects.get_or_create(
            type=ManuscriptItem.TYPE_VG_RESULT,
            manuscript=current_manuscript,
            order=2,
            text='Du har nå gått gjennom alle spørsmålene vi har for denne kategorien, og her partiene vi tror du er '
                 'mest enig i.'
        )
        ManuscriptItem.objects.get_or_create(
            type=ManuscriptItem.TYPE_QUICK_REPLY,
            manuscript=current_manuscript,
            order=3,
            text='Om du vil kan du velge en annen kategori og besvare spørsmålene for å gjøre vår gjetting bedre.',
            reply_text_1='De andre kategoriene',
            reply_action_1=root_manuscript
        )

    def create_manuscript_item_that_links_to_next_manuscript(self, current_manuscript, next_manuscript):
        ManuscriptItem.objects.get_or_create(
            type=ManuscriptItem.TYPE_QUICK_REPLY,
            manuscript=current_manuscript,
            order=2,
            text='Vil du se foreløpig resultat, eller vil du gå videre til neste spørsmål?',
            reply_text_1='Foreløpig resultat',
            reply_text_2='Neste spørsmål',
            reply_action_2=next_manuscript
        )
        ManuscriptItem.objects.get_or_create(
            type=ManuscriptItem.TYPE_VG_RESULT,
            manuscript=current_manuscript,
            order=3,
            text='Her er foreløpige resultat for partiene vi tror du er mest enig i'
        )
        # Note: Not needed, TYPE_VG_RESULT generates this response
        # ManuscriptItem.objects.get_or_create(
        #     type=ManuscriptItem.TYPE_QUICK_REPLY,
        #     manuscript=current_manuscript,
        #     order=4,
        #     text='Når du er klar kan du gå videre til å se neste spørsmål.',
        #     reply_text_1='Neste spørsmål',
        #     reply_action_1=next_manuscript
        # )

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

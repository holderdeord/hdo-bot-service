import csv

import sys

from django.core.management import BaseCommand
import requests

from quiz.models import Promise, Category, Party, HdoCategory
from quiz.utils import get_google_sheet_data, get_promise_id

import logging


class Command(BaseCommand):
    """
    Import checked promises from spreadsheet merged with matching HDO API data.

    Ref: https://data.holderdeord.no/api/promises/

    """

    HDO_API_URL = 'https://data.holderdeord.no/api/promises/'

    def add_arguments(self, parser):
        parser.add_argument('--category-map', type=str, default='./file/category_map.csv',
                            help='Path to file with mapping between categories and HDO categories')
        # Figured it is easier/better to just use the existing APIs to handle promises
        parser.add_argument('--all', action='store_true', help='Import _all_ promises from Holder de ord API')
        parser.add_argument('--check-file', type=str, help='Path to check file in CSV format')
        parser.add_argument('--google', action='store_true', help='Fetch promise check data from Google Spreadsheet')

    def handle(self, *args, **options):
        category_map = self.get_category_map(options['category_map'])

        if options['google']:
            checked_promises = self.get_promise_check_data_from_google_sheet
            promises = self.get_promises(checked_promises)
        elif options['check_file']:
            checked_promises = self.get_promise_check_data_from_file(options['check_file'])
            promises = self.get_promises(checked_promises)
        elif options['all']:
            promises = {}
            links_next = {
                'href': 'https://data.holderdeord.no/api/promises'
            }
            while links_next is not None:
                promises, links_next = self.get_promises_from_api(links_next['href'], promises)
            self.stdout.write('Downloaded {} promises from API'.format(len(promises)), ending='\n')
        else:
            self.stderr.write('Provide at least one of --all --google or --check-file', ending='\n')
            sys.exit(1)

        new_promises, updated_promises = self.create_or_update_promise_objects(promises, category_map)

        self.stdout.write('Imported {} new promise(s), updated {} promise(s)'.format(
            len(new_promises), len(updated_promises)), ending='\n')

    def get_promises(self, checked_promises):
        self.stdout.write('Found {} checked promise(s) in spreadsheet'.format(len(checked_promises)), ending='\n')

        api_data = self.get_promise_api_data(checked_promises.keys())

        return self.merge_api_and_check_data(checked_promises, api_data)

    def create_or_update_promise_objects(self, promises, category_map):
        new_promises = []
        updated_promises = []
        for external_id, p_data in promises.items():
            if p_data.get('body') is None:
                # FIXME: Skip empty promises for now, why empty?
                continue

            cats_data = p_data.pop('categories') if p_data.get('categories') else None
            parties_data = p_data.pop('parties') if p_data.get('parties') else None

            p, created = Promise.objects.get_or_create(external_id=external_id, defaults=p_data)
            if created:
                new_promises.append(p)
            else:
                # update fields
                changed = False
                for k, v in p_data.items():
                    if getattr(p, k) != v:
                        setattr(p, k, v)
                        changed = True
                if changed:
                    updated_promises.append(p)
                    p.save()

            if cats_data:
                # Note: inefficient
                cats = [Category.objects.get_or_create(name=cat)[0] for cat in cats_data]
                p.categories.add(*cats)
                hdo_categories = [category_map[category_name][0] for category_name in cats_data] if cats_data[0] != '' else []
                p.hdo_categories.add(*hdo_categories)

            if parties_data:
                # Note: inefficient
                parties = [Party.objects.get_or_create(title=p['title'], slug=p['slug'])[0] for p in parties_data]
                p.parties.add(*parties)

        return new_promises, updated_promises

    def merge_api_and_check_data(self, checked_promises, api_data):
        promises = checked_promises
        for p_data in api_data:
            _id = get_promise_id(p_data)
            new_data = {
                'body': p_data['body'],
                'parliament_period_name': p_data['parliament_period_name'],
                'promisor_name': p_data['promisor_name'],
                'source': p_data['source'],
                'parties': [{'title': party['title'], 'slug': party['slug']} for party in p_data['_links']['parties']]
            }
            promises[_id].update(new_data)

        return promises

    def get_promise_api_data(self, ids):
        if not ids:
            return []

        def chunks(l, n):
            """Yield successive n-sized chunks from l."""
            for i in range(0, len(l), n):
                yield l[i:i + n]

        max_ids = 400  # prevent too long GET param
        ids = sorted(ids)
        promises_paged = []
        for id_range in chunks(ids, max_ids):
            id_range = ','.join(id_range)
            total_pages = requests.get(self.HDO_API_URL, {'ids': id_range}).json()['total_pages']
            for page in range(total_pages):
                self.stdout.write('Fetching promises from {} (page {})'.format(self.HDO_API_URL, page), ending='\n')

                request_params = {'page': page, 'ids': id_range}
                res = requests.get(self.HDO_API_URL, request_params)
                res_data = res.json()

                promises_paged += res_data['_embedded']['promises']

        return promises_paged

    def get_promise_check_data_from_google_sheet(self):
        def _sheet_rows_to_dict(l):
            cols = l[0]
            return [dict(zip(cols, i)) for i in l[1:]]

        rows = get_google_sheet_data()
        if not rows:
            return {}

        return self.format_for_db(_sheet_rows_to_dict(rows))

    def get_promises_from_api(self, url, promises):
        document = requests.get(url).json()
        promises_data = document['_embedded']['promises']
        for p_data in promises_data:
            _id = get_promise_id(p_data)
            promises[_id] = {
                'external_id': int(_id),
                'categories': p_data['category_names'],
                'body': p_data['body'],
                'promisor_name': p_data['promisor_name'],
                'parliament_period_name': p_data['parliament_period_name'],
                'source': p_data['source'],
                'parties': [{'title': party['title'], 'slug': party['slug']} for party in p_data['_links']['parties']]
            }
        # Parsing next document, if available
        links_next = document['_links']['next'] if 'next' in document['_links'] else None
        # if links_next:
        #     self.get_promises_from_api(links_next['href'], promises)
        return promises, links_next

    def format_for_db(self, rows):
        promises = {}
        for row in rows:
            # Filter out promises that is not checked yet
            if not row.get('Holdt?') or not row.get('ID'):
                continue
            _id = self.parse_row_id(row['ID'])

            # Note: Mapping from spreadsheet column name to database column name
            category_names = row['Kategori'].split(';')
            # hdo_categories = [category_map[category_name][0] for category_name in category_names] if category_names[0] != '' else []
            promises[_id] = {
                'external_id': int(_id),
                'status': self.parse_status(row['Holdt?']),
                'categories': category_names,
                # 'hdo_categories': hdo_categories,
                'testable': self.parse_testable(row.get('Svada', '')),
                'description': row['Kommentar/Forklaring']
            }
        return promises

    def get_promise_check_data_from_file(self, check_file):
        with open(check_file) as f:
            csv_file = csv.DictReader(f)
            rows = [row for row in csv_file]

        return self.format_for_db(rows)

    def parse_status(self, val):
        val = val.lower().strip()
        _map = {
            'ja': Promise.FULFILLED,
            'nei': Promise.BROKEN,
            'delvis': Promise.PARTIAL,
            'ikke enda': Promise.NOT_YET_FULFILLED
        }
        return _map.get(val, '')

    def parse_testable(self, val):
        val = val.lower().strip()
        return val != 'nei'

    def parse_row_id(self, _id):
        return _id.strip().split('-')[0]

    def get_category_map(self, file_name):
        mapper = {}
        with open(file_name) as f:
            csv_file = csv.DictReader(f)
            for row in csv_file:
                mapper[row['Storting']] = list(map(self.get_hdo_category_id, row['HDO'].split('; ')))
        return mapper

    def get_category_id(self, category_name):
        return Category.objects.get_or_create(name=category_name)[0].pk

    def get_hdo_category_id(self, hdo_category_name):
        return HdoCategory.objects.get_or_create(name=hdo_category_name)[0].pk
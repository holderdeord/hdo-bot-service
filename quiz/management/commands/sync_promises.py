import csv

import sys

from django.core.management import BaseCommand
import requests

from quiz.models import Promise, Category, Party
from quiz.utils import get_google_sheet_data


class Command(BaseCommand):
    """
    Import checked promises from spreadsheet merged with matching HDO API data.

    Ref: https://data.holderdeord.no/api/promises/

    """

    HDO_API_URL = 'https://data.holderdeord.no/api/promises/'

    def add_arguments(self, parser):
        parser.add_argument('--check-file', type=str, help='Path to check file in CSV format')
        parser.add_argument('--google', action='store_true', help='Fetch promise check data from Google Spreadsheet')

    def handle(self, *args, **options):
        if options['google']:
            checked_promises = self.get_promise_check_data_from_google_sheet()
        elif options['check_file']:
            checked_promises = self.get_promise_check_data_from_file(options['check_file'])
        else:
            self.stderr.write('Either --google or --check-file needs to provided', ending='\n')
            sys.exit(1)

        self.stdout.write('Found {} checked promise(s) in spreadsheet'.format(len(checked_promises)), ending='\n')

        api_data = self.get_promise_api_data(checked_promises.keys())

        promises = self.merge_api_and_check_data(checked_promises, api_data)

        new_promises, updated_promises = self.create_or_update_promise_objects(promises)

        self.stdout.write('Imported {} new promise(s), updated {} promise(s)'.format(
            len(new_promises), len(updated_promises)), ending='\n')

    def create_or_update_promise_objects(self, promises):
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

            if parties_data:
                # Note: inefficient
                parties = [Party.objects.get_or_create(title=p['title'], slug=p['slug'])[0] for p in parties_data]
                p.parties.add(*parties)

        return new_promises, updated_promises

    def merge_api_and_check_data(self, checked_promises, api_data):
        promises = checked_promises
        for p_data in api_data:
            _id = p_data['_links']['self']['href'].split('/')[-1]
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

    def format_for_db(self, rows):
        promises = {}
        for row in rows:
            # Filter out promises that is not checked yet
            if not row.get('Holdt?') or not row.get('ID'):
                continue
            _id = self.parse_row_id(row['ID'])

            # Note: Mapping from spreadsheet column name to database column name
            promises[_id] = {
                'external_id': int(_id),
                'status': self.parse_status(row['Holdt?']),
                'categories': row['Kategori'].split(';'),
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

import csv
from django.core.management import BaseCommand
import requests

from quiz.models import Promise, Category, Party


class Command(BaseCommand):
    """
    Import checked promises from spreadsheet merged with matching HDO API data.

    Ref: https://data.holderdeord.no/api/promises/

    """
    # TODO: Could import check data directly from google spreadsheet

    HDO_API_URL = 'https://data.holderdeord.no/api/promises/'

    def add_arguments(self, parser):
        parser.add_argument('CHECK_FILE', type=str, help='Path to check file in CSV format')

    def handle(self, *args, **options):

        checked_promises = self.get_promise_check_data(options['CHECK_FILE'])
        api_data = self.get_promise_api_data(checked_promises.keys())

        promises = self.merge_api_and_check_data(checked_promises, api_data)

        new_promises = self.create_promises(promises)

        self.stdout.write('Imported {} new promises'.format(len(new_promises)), ending='\n')

    def create_promises(self, promises):
        new_promises = []
        for external_id, p_data in promises.items():
            cats_data = p_data.pop('categories') if p_data.get('categories') else None
            parties_data = p_data.pop('parties') if p_data.get('parties') else None

            p, created = Promise.objects.get_or_create(external_id=external_id, defaults=p_data)
            if created:
                new_promises.append(p)

            if cats_data:
                # Note: inefficient
                cats = [Category.objects.get_or_create(name=cat)[0] for cat in cats_data]
                p.categories.add(*cats)

            if parties_data:
                # Note: inefficient
                parties = [Party.objects.get_or_create(title=p['title'], slug=p['slug'])[0] for p in parties_data]
                p.parties.add(*parties)
        return new_promises

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

    def get_promise_api_data(self, ids, page=1):
        ids = ','.join(sorted(ids))

        has_next = True
        promises_paged = []
        while has_next:
            self.stdout.write('Fetching promises from {} (page {})'.format(self.HDO_API_URL, page), ending='\n')

            request_params = {'page': page, 'ids': ids}
            res = requests.get(self.HDO_API_URL, request_params)
            res_data = res.json()

            promises_paged += res_data['_embedded']['promises']

            has_next = res_data['_links'].get('next') is not None
            page += 1

        return promises_paged

    def get_promise_check_data(self, check_file):
        promises = {}
        with open(check_file) as f:
            csv_file = csv.DictReader(f)
            for row in csv_file:
                # Filter out promises that is not checked yet
                if not row['Holdt?']:
                    continue

                # Note: Mapping from spreadsheet column name to database column name
                promises[row['ID']] = {
                    'external_id': row['ID'],
                    'status': self.parse_status(row['Holdt?']),
                    'categories': row['Kategori'].split(';'),
                    'testable': self.parse_testable(row['Svada'])
                }

        return promises

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

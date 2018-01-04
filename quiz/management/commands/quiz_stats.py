import csv

from django.core.management import BaseCommand

from quiz.stats import counts_per_day


class Command(BaseCommand):
    """ Stats <3 """

    def add_arguments(self, parser):
        parser.add_argument('--csv', action='store_true', default=False, help='Format as CSV')

    def handle(self, *args, **options):
        counts = counts_per_day()
        if options['csv']:
            writer = csv.writer(self.stdout)
            writer.writerow(['Date', 'Count'])
            writer.writerows(counts)
        else:
            for c in counts:
                print(c[0], c[1])

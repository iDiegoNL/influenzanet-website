from optparse import make_option
from django.core.management.base import CommandError, BaseCommand

class Command(BaseCommand):
    help = 'Update all charts and invalidate tile cache.'
    option_list = BaseCommand.option_list

    def handle(self, *args, **options):
        from apps.pollster import models

        verbosity = int(options.get('verbosity'))

        for chart in models.Chart.objects.all():
            chart.update_data()
            if verbosity > 0:
                print 'Chart "%s" updated' % (chart,)

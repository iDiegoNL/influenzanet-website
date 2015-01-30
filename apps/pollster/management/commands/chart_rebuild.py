from optparse import make_option
from django.core.management.base import CommandError, BaseCommand

class Command(BaseCommand):
    help = 'Update all charts and invalidate tile cache.'
    option_list = BaseCommand.option_list +
        make_option('-c', '--chart', action='store', type="string",
                    dest='chart',
                    help='Chart name'),   
    def handle(self, *args, **options):
        from apps.pollster import models

        verbosity = int(options.get('verbosity'))
        
        chart = options['chart']
        
        if chart is not None:
            charts = models.Chart.objects.get(shortname=chart)
        else:
            charts = models.Chart.objects.all()

        for chart in chart:
            print "building chart %s" % (chart,)
            if not chart.update_table(verbose=verbosity > 0):
                print 'Chart "%s" update FAILED' % (chart,)
            elif verbosity > 0:
                print 'Chart "%s" updated' % (chart,)

from django.core.management.base import CommandError, BaseCommand
from ...models import EpiworkUser
from django.conf import settings
from optparse import make_option
from django.utils import simplejson

class Command(BaseCommand):
    help = 'Build domains list'

    option_list = BaseCommand.option_list + (
        make_option('-m', '--min', action='store', dest='min', default=10, help='Minimum number of mail to include the domain'),
    )

    def handle(self, *args, **options):
        domains = {}
        threshold = int(options['min'])
        verbose = options['verbosity'] > 0
        for user in EpiworkUser.objects.filter(is_active=True):
            email = user.email
            u, d = email.split('@')
            if domains.has_key(d):
                domains[d] = domains[d] + 1
            else:
                domains[d] = 1
                
        dd = []
        for (d,v) in domains.items():
            if verbose:
                print d + ":" + str(v)
            if int(v) >= threshold:
                dd.append(d)  
        domains = dd
        if len(domains) > 0:
            fn = settings.MEDIA_ROOT + '/assets/domains.json';
            f = file(fn,'w')
            s = simplejson.dumps(domains)
            f.write(s)
            f.close()
            print "%s updated" % fn
        else:
            print "No domain to include"
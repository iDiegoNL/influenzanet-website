import os
from django.core.management.base import CommandError, BaseCommand
from django.contrib.auth.models import User
from django.conf import settings
from optparse import make_option
from django.utils import simplejson

class Command(BaseCommand):
    help = 'Build domains list from user emails'

    option_list = BaseCommand.option_list + (
        make_option('-m', '--min', action='store', dest='min', default=10, help='Minimum number of mail to include the domain'),
        make_option('-o', '--output', action='store', dest='output', default='assets/domains.js', help='Output file path (relative to MEDIA_ROOT)'),
    )

    def handle(self, *args, **options):
        domains = {}
        threshold = int(options['min'])
        verbose = options['verbosity'] > 0
        for user in User.objects.filter(is_active=True):
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
            output = options['output']
            path = os.path.dirname(output)
            if not os.path.exists(path):
                os.makedirs(path)
            fn = settings.MEDIA_ROOT + os.path.sep + output;
            f = file(fn,'w')
            s = 'var my_domains = ' + simplejson.dumps(domains)+';'
            f.write(s)
            f.close()
            print "%s updated" % fn
        else:
            print "No domain to include"
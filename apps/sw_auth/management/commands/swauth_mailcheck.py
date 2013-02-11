from django.core.management.base import CommandError, BaseCommand
from ...models import EpiworkUser
from django.conf import settings

class Command(BaseCommand):
    help = 'Build domains list'

    def handle(self, *args, **options):
        domains = {}
        for user in EpiworkUser.objects.all():
            email = user.email
            u, d = email.split('@')
            if domains.has_key(d):
                ++domains[d]
            else:
                domains[d] = 1
        fn = settings.MEDIA_ROOT + '/sw/js/maildomains.js';
        f = file(fn,'w')
        s = " my_domains = ['"+ "','".join(domains.keys()) + "'];"
        f.write(s)
        f.close()
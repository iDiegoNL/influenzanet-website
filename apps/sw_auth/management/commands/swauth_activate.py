from optparse import make_option
from django.core.management.base import CommandError, BaseCommand
from ...models import EpiworkUser
from django.contrib.sites.models import Site
from apps.sw_auth.utils import send_activation_email

class Command(BaseCommand):
    help = 'manage activation'
    args = 'resend|clean'
    option_list = BaseCommand.option_list + (
        make_option('-u', '--user', action='store', dest='user', default=None, help='User id'),
    )

    def handle(self, *args, **options):
        try:
            command = args[0]
        except ValueError, IndexError:
            raise CommandError('Please enter a subcommand.')
        if options['user'] is None:
            users = EpiworkUser.objects.all()
        else:
            users = EpiworkUser.objects.get(id=options['user'])
    
        self.resend_activation(users)
    
    def resend_activation(self, users):
        site = Site.objects.get_current()
        for u in users:
            print "resend activation %s" % u.login
            send_activation_email(u, site)
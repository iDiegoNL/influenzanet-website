from optparse import make_option
from django.core.management.base import CommandError, BaseCommand
from ...models import EpiworkUser
from django.contrib.sites.models import Site
from apps.sw_auth.utils import send_activation_email

class Command(BaseCommand):
    help = 'manage activation'
    #args = 'resend|clean'
    option_list = BaseCommand.option_list + (
        make_option('-u', '--user', action='store', dest='user', default=None, help='User id'),
        make_option('-m', '--mail', action='store', dest='mail', default=None, help='User email'),
        make_option('-d', '--delay', action='store', dest='delay', default=None, help='Maximum delay from the user subscription to now (in days)'),
    )

    def handle(self, *args, **options):
        
        users = None
        
        if options['user'] is not None:
            users = [EpiworkUser.objects.get(id=options['user'])]
        
        if options['user'] is not None:
            users = [EpiworkUser.objects.get(id=options['user'])]
        
        if users is None:
            users = EpiworkUser.objects.filter(is_active=False)
        
        self.resend_activation(users)
    
    def resend_activation(self, users):
        site = Site.objects.get_current()
        for u in users:
            dju = u.get_django_user()
            print "resend activation %s" % u.login
            
            send_activation_email(u, site, renew=False)
from optparse import make_option
from django.core.management.base import CommandError, BaseCommand
from ...models import EpiworkUser
from django.contrib.auth.models import User
from django.conf import settings

class Command(BaseCommand):
    help = 'Transfert account to Test environnment'

    option_list = BaseCommand.option_list + (
        make_option('-u', '--user', action='store', dest='user', default=None, help='User id'),
    )

    def handle(self, *args, **options):
        if not getattr('SWAUTH_TEST_ENV', settings, False):
            print 'Not in test env'
            return
        
        # Remove all epiworkUser
        EpiworkUser.objects.all().delete()
        
        raw_password = settings.SWAUTH_TEST_PASS
        
        # Create Epiworkusers based on
        for user in User.objects.all():
            login = 'user'+user.id
            # Epiworkuser
            ew = EpiworkUser()
            ew.set_password(raw_password)
            ew.set_user(user.username)
            if user.is_staff:
                ew.login = user.username
            else:
                ew.login = 'user' + user.id
            ew.email = ew.login + '@localhost'
            ew.is_active = user.is_active
            ew.save()
            # user.save()
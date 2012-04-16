from django.core.management.base import CommandError, BaseCommand
from optparse import make_option
from registration.models import RegistrationProfile
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
import datetime

class Command(BaseCommand):
    help = 'Register a survey specification.'
    option_list = BaseCommand.option_list + (
        make_option('-f', '--fake', action='store_true',
            dest='fake', default=False,
            help='Fake the resent (show list).'),
        make_option('-u', '--user', action='store', type='string',
                dest='user', default=None,
                help='ID of user to resend.'),
        make_option('-r', '--renew', action='store_true', dest='renew', default=False,
                help='renew activation (set user date_joined to today)'),
    )
    
    
    def handle(self, *args, **options):
        
        user = options.get('user')
        fake = options.get('fake')
        renew = options.get('renew')
        
        site = Site.objects.get_current()
    
        if user is None:
            users = User.objects.filter(is_active=False)
        else:
            users = User.objects.filter(id=user)
    
        if len(users) == 0:
            print 'Nothing to resend'
            return
        
        print "%d user(s) to scan " % len(users)        
        for u in users:
            profile = RegistrationProfile.objects.get(user=u)
            resend = False
            if not profile.activation_key_expired:
                resend = True
            else:
                if renew:
                    u.date_joined = datetime.datetime.now()
                    u.save()
                    resend = True
                else:    
                    print 'Activation expired for user %d' % u.id
            if resend:
                profile.send_activation_email(site)


from django.core.management.base import CommandError, BaseCommand
from optparse import make_option
from django.core.mail import send_mail
from django.template.loader import render_to_string
from registration.models import RegistrationProfile
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Register a survey specification.'
    option_list = BaseCommand.option_list + (
        make_option('-f', '--fake', action='store_true',
            dest='fake', default=False,
            help='Fake the resent (show list).'),
        make_option('-u', '--user', action='store', type='string',
                dest='user', default=None,
                help='Login of user to resend.'),
    )
    
    def handle(self, *args, **options):
        
        user = options.get('user')
        fake = options.get('fake')
        if user is None:
            users = User.objects.filter(is_active=False)
        else:
            users = User.objects.filter(login=user)
        
        for u in users:
            profile = RegistrationProfile.objects.get(user=u)
            if not profile.activation_key_expired:
                print u


from optparse import make_option
from django.core.management.base import CommandError, BaseCommand
from ...models import EpiworkUser
from django.contrib.sites.models import Site
from apps.sw_auth.utils import send_activation_email

from django.core.validators import email_re

def is_email_valid(email):
    return bool(email_re.match(email))

class Command(BaseCommand):
    help = 'allow to change some user email'
    option_list = BaseCommand.option_list + (
        make_option('-m', '--mail', action='store', dest='mail', default=None, help='User email'),
        make_option('-n', '--new', action='store', dest='mail_new', default=None, help='New User email'),
        make_option('-a', '--activate', action='store_true', dest='activate', default=None, help='Resend activation with new email'),
    )

    

    def handle(self, *args, **options):
        
        if options['mail'] is None:
            raise CommandError('Mail is not provided')
        if options['mail_new'] is None:
            raise CommandError('new Mail is not provided')
        
        mail = options['mail']
        if not is_email_valid(mail):
            raise CommandError('email "%s" invalid' % mail)
        
        new_mail = options['mail_new']
        if not is_email_valid(new_mail):
            raise CommandError('email "%s" invalid' % new_mail)
        
        users = EpiworkUser.objects.filter(email=mail)
        
        activate = options['activate']
        
        if activate:
            site = Site.objects.get_current()
        
        if len(users) == 0:
            print 'User not found'
            return
        print "%d user(s) found" % len(users)
        print '----'
        for user in users:
            print "- User (id,login,mail): %d, %s, %s" % (user.id, user.login, user.email)
            confirm = raw_input("Confirm (yes/no) ")
            if confirm == "yes":
                user.email = new_mail
                user.save()
                print "user email changed to %s" % user.email
                if activate:
                    send_activation_email(user, site)
                    print "activation sended"

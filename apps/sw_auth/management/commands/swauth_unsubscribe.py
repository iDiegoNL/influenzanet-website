from optparse import make_option
from django.core.management.base import BaseCommand
from ...models import EpiworkUser
from django.contrib.auth.models import User
from django.core.validators import email_re
from apps.reminder.models import UserReminderInfo

def is_email_valid(email):
    return bool(email_re.match(email))

class Command(BaseCommand):
    help = 'unsubscribe user from the newsletter'
    option_list = BaseCommand.option_list + (
        make_option('-m', '--mail', action='store', dest='mail', default=None, help='User mail'),
        make_option('-f', '--file', action='store', dest='file', default=None, help='User mail in a file (one mail by line)'),
    )

    def unsubscribe_user(self, email):
        if not is_email_valid(email):
            print"[%s] Invalid email" % email
            return False 
        try:
            user = EpiworkUser.objects.get(email=email)
            django_user = user.get_django_user()
            try:
                info = UserReminderInfo.objects.get(user=django_user)
                if info.active:
                    info.active = False
                    info.save()
                    print "[%s] Unsubscribed" % email
                else:
                    print "[%s] Already inactive" % email
                return True
            except UserReminderInfo.DoesNotExist:
                print "[%s] User not registred for reminder" % email
                pass
        except EpiworkUser.DoesNotExist:
            print "[%s] User not found" % email
        except User.DoesNotExist:
            print "[%s] Django user not found" % email
        return False

    def handle(self, *args, **options):
        if options['mail']:
            self.unsubscribe_user(options['mail'])
        if options['file'] is not None:
            f = None
            count = 0
            try:
                f = open(options['file'], 'r')
                for mail in f:
                    mail = mail.strip()
                    if mail == '':
                        continue
                    if self.unsubscribe_user(mail):
                        ++count
            finally:
                if f is not None:
                    f.close()
        
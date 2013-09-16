from django.core.management.base import CommandError, BaseCommand
from optparse import make_option
from ...models import EpiworkUser
from ...anonymize import Anonymizer

from datetime import date, datetime

class Command(BaseCommand):
    help = 'Unsubscribing management of old accounts.'
    option_list = BaseCommand.option_list + (
        make_option('-f', '--fake', action='store_true',
            dest='fake', default=False,
            help='Fake the resent (show list).'),
    )     
    
    def delay(self, d):
        """
        Delay in days
        """
        if d is None:
            return None
        if isinstance(d, datetime):
            d = d.date()
        delay = date.today() - d
        return delay.days
    
    def fake(self, action, user):
        print " + [fake] %s for user %d" % (action, user.id)
    
    
    def handle(self, *args, **options):
                
        # fake the action
        fake = options.get('fake')
                
        users = EpiworkUser.objects.filter(is_active=True)

        anonymizer = Anonymizer()

        max_delay = anonymizer.login_delay # delay from last login
        waiting_delay = anonymizer.waiting_delay # waiting delay between warning and deactivation
        
        for user in users:
            dju = user.get_django_user()
            login_delay = self.delay(dju.last_login) 

            if user.anonymize_warn is not None:
                anonymize_delay = self.delay(user.anonymize_warn)
                if anonymize_delay >= login_delay:
                    # The user has been connected after the warning 
                    # Reactivate the account
                    if not fake:
                        anonymizer.cancel(user)
                    else:
                        self.fake('cancel', user)
                else:
                    if anonymize_delay > waiting_delay:
                        if not fake:
                            try:
                                anonymizer.anonymize(user)
                                print user.id + " anonymized" 
                            except:
                                print "Error during anonymization of user %d " % user.id
                        else:
                            self.fake('anonymize', user)
                    else:
                        print "User %d will be anonymized in %d days (if no login)" % (user.id, anonymize_delay - waiting_delay)
            else:
                # No warning            
                if login_delay > max_delay:
                    if not fake:
                        anonymizer.warn(user)
                    else:
                        self.fake('warn', user)

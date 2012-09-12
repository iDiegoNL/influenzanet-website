from optparse import make_option
from datetime import datetime, timedelta

from django.core.management.base import BaseCommand

from django.conf import settings as app_config

from ...send import send
from ...models import get_settings, UserReminderInfo, MockNewsLetter
from django.db import connection
from django.contrib.auth.models import User 

if getattr(app_config, 'SWAUTH_FAKE_USER', 0):
    from apps.sw_auth.models import EpiworkUserProvider as UserProvider
else:
    # Default User list provider
    class UserProvider(object):
        
        def __init__(self):
            self.users = User.objects.filter(is_active=True)  
            self.iter = None
        
        def __iter__(self):
            self.iter = self.users.__iter__()
            return self # return self to force use of our next() method
        
        def get_by_id(self, id):
            return User.objects.get(id=id)

        def get_by_login(self, login):
            return User.objects.get(username=login)
        
        def next(self): 
            return next(self.iter)    

class Command(BaseCommand):
    help = "Send reminders."

    option_list = BaseCommand.option_list + (
        make_option('--fake', action='store_true', dest='fake', default=False, help='Fake the sending of the emails; print the emails to be sent on screen instead.'),
        make_option('--user', action='store', dest='user', default=None, help='Send only to this user (user login)'),
        make_option('--verbose', action='store_true', dest='verbose', default=False, help='Print verbose message'),
        make_option('--counter', action='store', dest='counter', default=None, help='Store counter value into this file'),
        make_option('--log', action='store', dest='log', default=None, help='Store user email in a log file'),
        make_option('--next', action='store', dest='next', default=None, help='Next url for login url'),
        make_option('--mock', action='store_true', dest="mock", default=False, help="Create a mock newsletter and fake send it (always fake)"),
    )

    def __init__(self):
        super(BaseCommand, self).__init__()
        self.log = None
        self.fake = False

    def get_reminder(self):
        query = "SELECT n.id, subject, message, sender_email, sender_name, date FROM reminder_newslettertranslation t left join reminder_newsletter n on n.id=t.master_id where t.language_code='fr' and published=True order by date desc"
        cursor = connection.cursor()
        cursor.execute(query)
        res = cursor.fetchone()
        reminder = MockNewsLetter()
        reminder.subject = res[1]
        reminder.message = res[2]
        reminder.sender_email = res[3]
        reminder.sender_name = res[4]
        reminder.date = res[5]
        return reminder
           
    def get_mock_reminder(self):
        reminder = MockNewsLetter()
        reminder.subject = "Mock newsletter"
        reminder.message = "Lorem ipsum"
        reminder.sender_email = "mock@localhost"
        reminder.sender_name = "mock"
        reminder.date = datetime.now()
        return reminder
        
    def send_reminders(self, message, target, next, batch_size):
        
        now = datetime.now()
        
        users = UserProvider()
        
        if self.verbose:
            print "> User provider class : %s " % str(users.__class__)
        
        if(target is not None):
            print "> target user=%s" % (target)
            users = [ users.get_by_login(target) ]
            print users

        i = -1
        language = 'fr'
        print "next=%s" % (next)
        try:
            for user in users :
                if batch_size and i >= batch_size:
                    raise StopIteration 
                
                to_send = False
                
                info, _ = UserReminderInfo.objects.get_or_create(user=user, defaults={'active': True, 'last_reminder': user.date_joined})
    
                if not info.active:
                    continue
                
                if info.last_reminder is None:
                    to_send = True
    
                if info.last_reminder < message.date:
                    to_send = True    
            
                if to_send:
                    i += 1
                    if not self.fake:
                        if(self.verbose):
                            print 'sending', user.email 
                        send(now, user, message, language, next=next)
                    else:
                        print '[fake] sending', user.email, message.subject
        except StopIteration:
            pass
        return i + 1

    def handle(self, *args, **options):
        self.fake    = options.get('fake', False)
        self.log = options.get('log', None)
        self.verbose = options.get('verbose', False)
        
        user    = options.get('user', None)
        counter = options.get('counter', None)
        next = options.get('next', None)
        mock = options.get('mock', False)
        
        conf = get_settings()
        
        if conf is None:
            return u"0 reminders sent - not configured"
        else:
            if conf.currently_sending and conf.last_process_started_date + timedelta(hours=3) > datetime.now():
                return u"0 reminders sent - too soon"

        batch_size = conf.batch_size

        conf.currently_sending = True
        conf.last_process_started_date = datetime.now()
        conf.save()
        
        try:
            if mock:
                message = self.get_mock_reminder()
                self.fake = True
            else:
                message = self.get_reminder()
            
            count = self.send_reminders(message=message, target=user, batch_size=batch_size, next=next)
        
            if(counter is not None):
                file(counter,'w').write(str(count))
            return u'%d reminders sent.\n' % count 
       
        finally:
            conf = get_settings()
            conf.currently_sending = False
            conf.save()
            

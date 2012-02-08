from optparse import make_option
from datetime import datetime, timedelta

from django.core.management.base import BaseCommand

from django.contrib.auth.models import User

from ...send import get_reminders_for_users, send
from ...models import get_settings
from django.db import connection

class Command(BaseCommand):
    help = "Send reminders."

    option_list = BaseCommand.option_list + (
        make_option('--fake', action='store_true', dest='fake', default=False, help='Fake the sending of the emails; print the emails to be sent on screen instead.'),
        make_option('--user', action='store', dest='target', default=None, help='Send only to this user (user id)'),
        make_option('--verbose', action='store_true', dest='verbose', default=False, help='Print verbose message'),
        make_option('--counter', action='store', dest='counter', default=None, help='Store counter value into this file'),
        make_option('--log', action='store', dest='log', default=None, help='Store user email in a log file'),
    )

    def get_reminder(self, reminder):
       query = "SELECT n.id, subject, message, sender_email, sender_name,date FROM reminder_newslettertranslation t left join reminder_newsletter n on n.id=t.master_id where t.language_code='fr' and published=True order by date desc"
       cursor = connection.cursor()
       cursor.execute(query)
       return cursor.fetchone()
    
    def send_reminders(self, fake, target, verbose, log):
        now = datetime.now()
        if(target is not None):
            users = User.objects.get(id=target)
        else:
            users = User.objects.filter(is_active=True) 
        i = -1
        print self.get_reminder('toto')
        for i, (user, message, language) in enumerate(get_reminders_for_users(now, users)):
            if not fake:
                if(verbose):
                    print 'sending', user.email
                    
                send(now, user, message, language)
            else:
                print '[fake] sending', user.email, message.subject
    
        return i + 1

    def handle(self, *args, **options):
        fake    = options.get('fake', False)
        user    = options.get('user', None)
        verbose = options.get('verbose', False)
        counter = options.get('counter', None)
        log = options.get('log', None)
        
        if not get_settings():
            return u"0 reminders sent - not configured"

        if get_settings() and get_settings().currently_sending and\
            get_settings().last_process_started_date + timedelta(hours=3) > datetime.now():
            return u"0 reminders sent - too soon"

        settings = get_settings()
        settings.currently_sending = True
        settings.last_process_started_date = datetime.now()
        settings.save()
        try:
            count = self.send_reminders(fake=fake, target=user, verbose=verbose, log=log)
            if(counter is not None):
                file(counter,'w').write(str(count))
            return u'%d reminders sent.\n' % count 
        finally:
            settings = get_settings()
            settings.currently_sending = False
            settings.save()
            

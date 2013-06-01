## Handle anonymization of account
from django.core.urlresolvers import reverse
from .models import AnonymizeLog
import datetime
from .utils import send_user_email

class Anonymizer:
    
    def __init__(self):
        self.waiting_delay = 12
        self.login_delay = 30*18
    
    def log(self, user, event):
        """
        Log an event on the user account
        """
        l = AnonymizeLog()
        l.user = user
        l.event = event
        l.save()
    
    def send_anonymized(self, user_id, user_email):
        # Send an email to tell the user his account has been anonymized
        send_user_email('account_deactivated', user_email, {'id':user_id})
        
    def send_warning(self, user ):
        expires = datetime.datetime.now() + datetime.timedelta(days=self.waiting_delay + 1)
        next = reverse('deactivate_planned')
        token = user.create_login_token(usage_left=1, expires=expires, next=next)
        send_user_email('deactivate_warning', user.email, {'waiting_delay': self.waiting_delay, 'login_token':token.get_url()})
    
    def anonymize(self, user):
        email = user.email
        user.anonymize()
        self.send_anonymized(user.id, email)
        self.log(user, AnonymizeLog.EVENT_DONE)
    
    def warn(self, user, delay=None):
        d = datetime.date.today()
        if delay is not None:
            t = datetime.timedelta(days=delay)
            d = d + t 
        user.anonymize_warn = d
        user.save()
        self.log(user, AnonymizeLog.EVENT_WARNING)
        self.send_warning(user)
    
    def cancel(self, user):
        user.anonymize_warn = None
        user.save()
        self.log(user, AnonymizeLog.EVENT_CANCELLED)


        
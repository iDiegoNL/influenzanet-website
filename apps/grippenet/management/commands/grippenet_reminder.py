from django.core.management.base import BaseCommand
from optparse import make_option

from apps.grippenet.models import PregnantCohort
from django.core.urlresolvers import reverse
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags

import datetime

from apps.common.db import get_cursor
from apps.sw_auth.models import EpiworkUserProxy

from ...reminder import create_message

class Command(BaseCommand):
    help = 'Send Reminder about Pregnant survey'
    
    option_list = BaseCommand.option_list + (
        make_option('-s', '--survey', action='store', type="string", dest='survey',  help='Survey to redirect to'),
        make_option('-l', '--list', action='store', type="string",  dest='list', help='Participants from list'),
        make_option('-t', '--template', action='store', type="string",  dest='template', help='template name (without .html)'),
        make_option('-f', '--fake', action='store_true',  dest='fake', help='fake sending', default=False),
    )

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.template = ''
        self.survey = ''
        self.fake = False

    def send_email(self, user, gid, email):
        
        next = reverse('survey_fill', kwargs={'shortname': self.survey}) + '?gid=' + gid
        
        text_content, html_content = create_message(user, next=next, template=self.template +'.html' )
        
        text_content = strip_tags(text_content)
        msg = EmailMultiAlternatives(
            'Etude G-GrippeNet',
            body=text_content,
            to=[email],
            )

        msg.attach_alternative(html_content, "text/html")

        if self.fake:
            print '[fake]',
            return True
        
        try:
            msg.send()
            return True
        except Exception, e:
            print e
            return False
    
    def get_participants(self, listname):
        cursor = get_cursor()
        cursor.execute("SELECT id from %s" % (listname))
        results = cursor.fetchall()
        results = [r[0] for r in results] 
        
        p = PregnantCohort.objects.all().filter(survey_user__in=results)
        
        return p
    
    def get_respondents(self, survey):
        cursor = get_cursor()
        table = "pollster_results_%s" % (survey)
        cursor.execute("SELECT distinct s.id as person_id from %s p left join survey_surveyuser s on p.global_id=s.global_id" % (table))
        responsents = cursor.fetchall()
        respondents = [r[0] for r in responsents] 
        return respondents
    
    def handle(self, *args, **options):
        
        survey = options.get('survey')
        
        self.survey = survey
        
        self.template = options.get('template')
        
        self.fake = options.get('fake')
        
        list = options.get('list')
        
        now = datetime.date.today()
        
        participants = self.get_participants(list)
        
        provider = EpiworkUserProxy()
        
        # Get 
        respondents = self.get_respondents(survey)
        
        print "%d particpants to scan" % ( len(participants))
        for p in participants: 
            su = p.survey_user
            suid = su.id
            dju = su.user
            if suid in respondents:
                print "participant #%d already responded" % (suid,)
                continue 
    
            account = provider.find_by_django(dju)
            if account is not None:
                print "sending reminder to participant #%d <%s>" %(suid, account.email)
                if self.send_email(dju, su.global_id, account.email):
                    p.reminder_count = p.reminder_count + 1
                    p.date_reminder = now + datetime.timedelta(days=15) # future date
                    p.save()
            else:
                print "Unable to find email for participant #%d" %(suid,)
            
        
        
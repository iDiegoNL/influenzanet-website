from django.core.management.base import BaseCommand

from django.conf import settings
from apps.grippenet.models import PregnantCohort
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.core.mail import EmailMultiAlternatives
from django.template import Context, loader, Template
from django.utils.html import strip_tags
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django.utils.translation import activate

import loginurl.utils
from apps.partnersites.context_processors import site_context

import datetime
import loginurl

from apps.common.db import get_cursor
from apps.sw_auth.models import EpiworkUserProxy

def get_login_url(user, next):
    expires = datetime.datetime.now() + datetime.timedelta(days=30)

    usage_left = 5
    key = loginurl.utils.create(user, usage_left, expires, next)

    domain = Site.objects.get_current()
    path = reverse('loginurl-index').strip('/')
    loginurl_base = 'https://%s/%s' % (domain, path)

    return '%s/%s' % (loginurl_base, key.key)

def create_message(user, next=None):
    activate('fr')

    t = loader.get_template('pregnant.html')
    c = {
        'url': get_login_url(user, next),
    }
    c.update(site_context())
    
    site_url = 'https://%s' % Site.objects.get_current().domain
    media_url = '%s%s' % (site_url, settings.MEDIA_URL)
    
    c['site_url'] = site_url
    inner = t.render(Context(c))
    template = 'ggrippenet.html'
    t = loader.get_template(template)
    c['inner'] = inner
    c['MEDIA_URL'] = media_url
    return inner, t.render(Context(c))


class Command(BaseCommand):
    help = 'Send Reminder about Pregnant survey'
    
    def send_email(self, user, gid, email):
        
        next = reverse('survey_fill', kwargs={'shortname':'pregnant'}) + '?gid=' + gid
        
        text_content, html_content = create_message(user, next=next )
        
        text_content = strip_tags(text_content)
        msg = EmailMultiAlternatives(
            'Etude G-GrippeNet',
            body=text_content,
            to=[user.email],
            )

        msg.attach_alternative(html_content, "text/html")

        try:
            msg.send()
            return True
        except Exception, e:
            print e
            return False
    
    def handle(self, *args, **options):
        
        now = datetime.date.today()
        
        participants = PregnantCohort.objects.filter(date_reminder__lt=now)
        #participants = PregnantCohort.objects.all()[0:1]
        
        provider = EpiworkUserProxy()
        
        cursor = get_cursor()
        cursor.execute("SELECT distinct s.id as person_id from pollster_results_pregnant p left join survey_surveyuser s on p.global_id=s.global_id")
        responsents = cursor.fetchall()
        respondents = [r[0] for r in responsents] 
        
        print "%d particpants to scan" % ( len(participants))
        for p in participants: 
            su = p.survey_user
            suid = su.id
            dju = su.user
            
            if suid in respondents:
                print "participant #%d already responded" % (suid,)
                continue 
     
            if p.reminder_count > 2:
                print "participant #%d reached max reminders" % (suid,)
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
            
        
        
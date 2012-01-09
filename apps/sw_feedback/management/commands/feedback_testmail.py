recipientsfrom apps.count.sites import *
from django.conf import settings
from django.core.cache import cache
from django.core.management.base import NoArgsCommand, BaseCommand
from django.core.mail import send_mail


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
       
       recipients = [ x[1] for x in settings.ADMINS ]  
       send_mail('Test', 'Test', settings.DEFAULT_FROM_EMAIL, recipients)
  

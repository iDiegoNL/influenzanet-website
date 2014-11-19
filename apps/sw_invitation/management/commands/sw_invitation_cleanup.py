from django.conf import settings
from django.core.management.base import NoArgsCommand
from ...models import Invitation
import datetime

class Command(NoArgsCommand):
    
    def handle_noargs(self, **options):

        limit = datetime.datetime.now() - datetime.timedelta(days=365)
        
        print 'Anonymizing invitation older than one year or more'
        count = 0
        for invit in Invitation.objects.filter(date__lt=limit):
            ano = "anonymized-%d@localhost" % (invit.id,)
            if invit.email != ano:
                invit.email = ano  
                invit.save()
                count += 1
        print "%d invitations anonymized" % count
        
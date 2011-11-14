from django.core.management.base import NoArgsCommand

from ...send import send_reminders
from ...models import get_settings

class Command(NoArgsCommand):
    help = "Send reminders."

    def handle_noargs(self, **options):
        if get_settings() and get_settings().currently_sending:
            return u"0 reminders sent"

        settings = get_settings()
        settings.currently_sending = True
        settings.save()
        try:
            return u'%d reminders sent.\n' % send_reminders()
        finally:
            settings = get_settings()
            settings.currently_sending = False
            settings.save()
            

from optparse import make_option
from django.core.management.base import CommandError, BaseCommand
from ...models import EpiworkUser
from django.conf import settings
from django.contrib.sites.models import Site
from apps.sw_auth.utils import TOKEN_ACTIVATE, TOKEN_PASSWORD, TOKEN_EMAIL

class Command(BaseCommand):
    help = 'Cleanup tokens'
    args = 'activate|password|email|all'

    def handle(self, *args, **options):
        try:
            command = args[0]
            command.lower()
        except (ValueError, IndexError):
            raise CommandError('Please enter a subcommand.')

        tokens = {
            'activate' : { 'attr':'token_activate', 'type': TOKEN_ACTIVATE, 'delay': settings.ACCOUNT_ACTIVATION_DAYS },
            'password': { 'attr':'token_password', 'type': TOKEN_PASSWORD, 'delay': settings.ACCOUNT_ACTIVATION_DAYS },
            'email': { 'attr':'token_email', 'type': TOKEN_EMAIL, 'delay': 30 }
        }

        todo = [ command ]


        if command == 'all':
            todo = tokens.keys()
        else:
            if not tokens.has_key(command):
                raise CommandError('Invalid subcommand')

        for user in EpiworkUser.objects.all():

            for token_type in todo:
                should_save = False
                token_def = tokens[token_type]
                token = user.get_token(token_def['type'])
                if token.is_empty():
                    continue
                age = token.get_age()
                if age is None or age > token_def['delay']:
                    setattr(user, token_def['attr'], '')
                    print "user %d cleanup token %s[%s] " % (user.id, token.random, token.timestamp)
                    should_save = True
                if should_save:
                    user.save()

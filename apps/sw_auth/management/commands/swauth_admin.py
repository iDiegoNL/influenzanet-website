#from optparse import make_option
from django.core.management.base import CommandError, BaseCommand
from getpass import getpass
from ...models import EpiworkUser
from optparse import make_option
from django.contrib.auth import authenticate

class Command(BaseCommand):
    help = 'Manage admin actions'
    args = 'command'
    
    option_list = BaseCommand.option_list  + (
        make_option('-u', '--user', action='store', dest='user', default=None, help='User id'),
        make_option('-m', '--mail', action='store', dest='email', default=None, help='User email'),
    )

    def handle(self, *args, **options):
        
        try:
            command = args[0]
            command.lower()
        except (ValueError, IndexError):
            raise CommandError('Please enter a subcommand.')
        
        pwd = getpass("root django password : ")
        
        root = authenticate(username="root", password=pwd)
        
        if root is None:
            return
    
        if len(args) < 1:
            raise CommandError("User login is requirer as first argument")
        
        try:
            login = args[0]
        except ValueError, IndexError:
            raise CommandError('Please enter a user login.')
        
        try:
            user = EpiworkUser.objects.get(login=login)
            print "found user #%s %s" % (str(user.id), str(user.login))
            u = user.get_django_user()
            print "id=", u.id
            print "username=",u.username
            
        except EpiworkUser.DoesNotExist:
            print "user %s does not exists" % login
    
    def get_user(self, options):
        
        
    def handle_disclose(self, options):
        
#from optparse import make_option
from django.core.management.base import CommandError, BaseCommand
from ...models import EpiworkUser
from django.contrib.auth import authenticate

class Command(BaseCommand):
    help = 'Disclose a user'
    args = 'username'
    
    option_list = BaseCommand.option_list 
#    + (
#        make_option('-u', '--user', action='store', dest='user', default=None, help='User id'),
#    )

    def handle(self, *args, **options):
        
        pwd = raw_input("root django password : ")
        
        root = authenticate(username="root", password=pwd)
        
        if root is None:
            return
        
        try:
            login = args[0]
        except ValueError, IndexError:
            raise CommandError('Please enter a user login.')
        
        try:
            user = EpiworkUser.objects.get(login=login)
            print "found user",str(user)
            
        except EpiworkUser.DoesNotExist:
            print "user does not exists"
    

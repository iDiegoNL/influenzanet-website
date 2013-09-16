#from optparse import make_option
from django.core.management.base import CommandError, BaseCommand
from getpass import getpass
from ...models import EpiworkUser
from optparse import make_option
from django.contrib.auth import authenticate
from django.db import transaction
from django.db.models import Q

class Command(BaseCommand):
    help = 'Manage admin actions'
    args = 'disclose|makeadmin'
    
    option_list = BaseCommand.option_list  + (
        make_option('-u', '--user', action='store', dest='user', default=None, help='User id'),
        make_option('-m', '--mail', action='store', dest='email', default=None, help='User email'),
        make_option('-l', '--login', action='store', dest='login', default=None, help='User login'),
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
    
        # del args[0]
        
        user = self.get_user(options)
        
        if command == 'disclose':
            self.handle_disclose(user, options)
        elif command == 'makeadmin':
            self.handle_makeadmin(user, options)
    
    def get_user(self, options):
        user = None
        param = None
        try:
            if options['user'] is not None:
                param = Q(id=options['user'])
            elif options['login'] is not None:
                param = Q(login=options['login'])
            elif options['email'] is not None:
                param = Q(email=options['email'])
            else:
                print "No param"
            user = EpiworkUser.objects.get(param)

        except EpiworkUser.DoesNotExist:
            print "User not found with params %s" % str(param)
            pass
        if user is not None:
            print "found user #%s %s" % (str(user.id), str(user.login))
            
        return user
        
    def handle_disclose(self, user, options):
        if user is None:
            raise Exception('No user found')
        u = user.get_django_user()
        print "Django auth_user keys :"
        print "id=", u.id
        print "username=",u.username
    
    @transaction.commit_on_success
    def make_user_admin(self, user):
        u = user.get_django_user()
        u.is_staff = True
        u.password = user.password
        u.email = user.email
        u.username = user.login
        user.set_user(user.login)
        u.save()
        user.save()       

    def handle_makeadmin(self, user, options):
        if user is None:
            raise Exception('No user found')
        if not user.is_active:
            print "user account is not active"
            return
        confirm = raw_input("Confirm (y/n) ")
        confirm = confirm.lower()
        if confirm == 'y':
            self.make_user_admin(user)

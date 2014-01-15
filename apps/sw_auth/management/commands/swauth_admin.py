#from optparse import make_option
from django.core.management.base import CommandError, BaseCommand
from getpass import getpass
from ...models import EpiworkUser
from optparse import make_option
from django.contrib.auth import authenticate
from django.db import transaction
from django.db import connection
from django.db.models import Q
from apps.sw_auth.models import AnonymizeLog
from apps.survey.models import SurveyUser
from django.conf import settings

class Command(BaseCommand):
    help = 'Manage admin actions'
    args = 'disclose|makeadmin|anonymize'
    
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
            print "uh oh, wrong try"
            return
    
        # del args[0]
        print "Access granted"
        
        user = self.get_user(options)
        
        if command == 'disclose':
            self.handle_disclose(user, options)
        elif command == 'makeadmin':
            self.handle_makeadmin(user, options)
        elif command == 'anonymize':
            self.handle_anonymize(user, options)
    
    
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
        except EpiworkUser.MultipleObjectsReturned:
            print "Multiple user found with this params"
            pass
        if user is not None:
            print "found user #%s %s" % (str(user.id), str(user.login))
            
        return user
        
    def handle_disclose(self, user, options):
        if user is None:
            raise Exception('No user found')
        u = user.get_django_user()
        print "Django auth_user keys :"
        print "id=%d  username=%s" % ( u.id, u.username)
        self.show_user(u)
        
    def show_user(self, user):
        participants = SurveyUser.objects.filter(user=user)
        print "---------------------------------------"
        print "%d participants linked to this account" % len(participants)
        print "---------------------------------------"
        tables = {'intake':'pollster_results_intake', 'weekly':'pollster_results_weekly'}
        # handle historical tables data
        if hasattr(settings, 'HISTORICAL_TABLES'):
            h = settings.HISTORICAL_TABLES
            for season in h.keys():
                tb = h[season]
                tables[season+'_intake'] = tb['intake']
                tables[season+'_weekly'] = tb['weekly'] 
        data = []
        width = [6, 6]
        cols = ['id','active']
        for tb in tables.keys():
            cols.append(tb)
            width.append(len(tb))
            
        for participant in participants:
            d = [participant.id, (not participant.deleted)]
            for tb in tables.keys():
                cursor = connection.cursor()
                table = tables.get(tb)
                cursor.execute("SELECT count(*) from " + table+" where global_id='" + participant.global_id+"'")
                r = cursor.fetchone()
                d.append(r[0])
            data.append(d)
        
        i = 0
        for col in cols:
            mask = " % " + str(width[i])+"s " 
            print mask % col,
            i = i + 1
        print
        for d in data:
            i = 0
            for v in d:
                mask = " % " + str(width[i]) + "s " 
                print mask % str(v),
            print
    
    def handle_anonymize(self, user, options):
        confirm = raw_input("Confirm (yes/no) ")
        confirm = confirm.lower()
        if confirm == 'yes':
            user.anonymize()
            log = AnonymizeLog()
            log.user = user
            log.event = AnonymizeLog.EVENT_MANUALLY
            log.save()
    
    @transaction.commit_on_success
    def make_user_admin(self, user):
        u = user.get_django_user()
        if(u.is_staff):
            print "user %s is already admin, updating account"
        else:
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

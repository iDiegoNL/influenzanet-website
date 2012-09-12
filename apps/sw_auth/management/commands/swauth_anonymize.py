from django.core.management.base import CommandError, BaseCommand
from optparse import make_option
from django.contrib.auth.models import User,UNUSABLE_PASSWORD
from ...models import EpiworkUser
from apps.survey.models import SurveyUser
from django.db import transaction
from random import choice

# create a random string
def random_string(length, allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789'):
    return ''.join([choice(allowed_chars) for i in range(length)])

class Command(BaseCommand):
    help = 'Anonymize an account.'
    option_list = BaseCommand.option_list + (
        make_option('-f', '--fake', action='store_true',
            dest='fake', default=False,
            help='Fake the resent (show list).'),
        make_option('-u', '--user', action='store', type='string',
                dest='user', default=None,
                help='ID of user to resend.'),
        make_option('-m', '--mail', action='store', type='string',
                dest='mail', default=None,
                help='email of user to anoymize.'),
    )
    
    @transaction.commit_manually()
    def anonymize(self, ewuser):
        ''' anonymise a user 
        '''
        id = ewuser.id
        # create a unique user name (not used)
        name = 'user'+str(id)+'-'+random_string(6)
        ewuser.login = name
        ewuser.email = name+'@'+'localhost'
        ewuser.password = UNUSABLE_PASSWORD 
        ewuser.is_active = False
        
        # get the django user
        user = ewuser.get_django_user()
        # user = django user
        try:
            # remove participant info
            susers = SurveyUser.objects.filter(user=user)
            for su in susers:
                print " > anonymizing participant %d" % su.id
                su.name = 'part' + str(su.id) +'_'+random_string(4) # random tail to expect uniqueness
                su.save() 
            
            user.first_name = 'nobody'
            user.last_name = 'nobody'
            user.password = UNUSABLE_PASSWORD
            user.is_active = False
            user.save()
            ewuser.save()
            transaction.commit()
            print " > account %d anonymized" % id
        except Exception as e:
            print 'error during anonymization'
            transaction.rollback()
            print e
        
    
    def handle(self, *args, **options):
        
        # user id
        user_id = options.get('user')
        
        # fake the action
        fake = options.get('fake')
        
        # force to renew the activation
        mail = options.get('mail')
        
        if user_id is not None and mail is not None:
            print 'Either User id or email should be provided, not both'
            return

        if user_id is not None:
            u = user_id.split(',')
            users = EpiworkUser.objects.filter(id__in=u)
        else:
            users = EpiworkUser.objects.filter(email=mail)

        if len(users) == 0:
            print 'User not found'
            return
        print "%d user(s) found" % len(users)
        print '----'
        for user in users:
            print "- User (id,login,mail): %d, %s, %s" % (user.id, user.login, user.email)
            confirm = raw_input("Confirm (yes/no) ")
            if confirm == "yes":
                if fake:
                    print "fake anonymizing user %d" % user.id
                else:
                    self.anonymize(user)
            else:
                print "> Cancelled for user %d" % user.id

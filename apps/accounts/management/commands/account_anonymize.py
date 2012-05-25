from django.core.management.base import CommandError, BaseCommand
from optparse import make_option
from django.contrib.auth.models import User,UNUSABLE_PASSWORD
from apps.survey.models import SurveyUser
from django.db import transaction

class Command(BaseCommand):
    help = 'Resend activation mail to user(s).'
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
    def anonymize(self, user):
        id = user.id
        try:
            susers = SurveyUser.objects.filter(user=user)
            
            for su in susers:
                print "anonymizing participant %d" % su.id
                su.name = 'participant'+su.id
                su.save() 

            name = user+'id'
            user.email = name+'@'+'localhost'
            user.first_name = name
            user.last_name = name
            user.password = UNUSABLE_PASSWORD
            user.is_active = False
            user.save()
            print "account %d anonymized" % id
            transaction.commit()
        except:
            print 'error during anonymization'
            transaction.rollback()
        
    
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
            user = User.objects.get(id=user_id)
        else:
            user = User.objects.get(email=mail)

        if len(user) == 0:
            print 'User not found'
            return
        
        print "User found: %d" % user.id
        print "Name: %s %s " % (user.first_name, user.last_name)
        print "login: %s " % (user.username, user.last_name)
        print "email: %s " % (user.email)
        
        confirm = raw_input("Confirm (yes/no")
        if confirm == "yes":
            if fake:
                print "fake anonymizing user " % user.id
            else:
                self.anonymize(user)
        

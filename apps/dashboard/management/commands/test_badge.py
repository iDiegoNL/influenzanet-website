from optparse import make_option
from django.core.management.base import  BaseCommand, CommandError
from apps.survey.models import SurveyUser
from apps.dashboard.models import UserBadge
from django.core.exceptions import ObjectDoesNotExist

class Command(BaseCommand):
    help = 'test my badges a .'
    
    option_list = BaseCommand.option_list + (
        make_option('-g', '--gid', action='store',
                    dest='global_id', default=None,
                    help='Survey User to test'),
        make_option('-p', '--participant', action='store',
                    dest='participant', default=None,
                    help='Survey User (id) to test'),
    )
    
    def handle(self, *args, **options):
        
        global_id = options['global_id']
        if not global_id:
            raise CommandError("global_id must be provided")
        try :
            u = SurveyUser.objects.get(global_id=global_id)
        except ObjectDoesNotExist:
            raise CommandError("'%s' participant does not exist" % global_id)
        
        self.test_participant(u)

    def test_participant(self, u):
        manager = UserBadge.objects
        
        news = manager.update_badges(u, fake=True)
        
        badges = manager.get_badges()
        
        #  Index by id
        bb = { }
        for b in badges:
            bb[b.id] = b
        badges = bb 
        
        def show_badges(news):
            print "%d new badges " % len(news)
            for bid in news:
                badge = badges[ bid ]
                print badge.name
        
        if news:
            print "Badge for participant"
            print show_badges(news['participant'])
            print "Badge for user account"
            print show_badges(news['user'])
        else:
            print "no data ??"

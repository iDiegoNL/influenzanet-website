from optparse import make_option
from django.core.management.base import  BaseCommand
from apps.survey.models import SurveyUser
from apps.dashboard.models import UserBadge

class Command(BaseCommand):
    help = 'test my badges a .'
    
    def handle(self, *args, **options):
        
        u = SurveyUser.objects.get(global_id='471fbd68-977f-4f59-a4d1-7b73e666408d')
        
        manager = UserBadge.objects
        
        news = manager.update_badges(u, fake=False)
        
        badges = manager.get_badges()
        
        badges = { b.id:b for b in badges  }
        
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

        

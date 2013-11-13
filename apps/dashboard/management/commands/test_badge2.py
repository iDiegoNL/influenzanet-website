from optparse import make_option
from django.core.management.base import  BaseCommand, CommandError
from apps.survey.models import SurveyUser
from apps.dashboard.models import UserBadge
from django.core.exceptions import ObjectDoesNotExist
from django.db import connection
class Command(BaseCommand):
    help = 'test my badges a .'
        
    
    def get_value(self, query):
        cursor = connection.cursor()
        cursor.execute(query)
        d = cursor.fetchone()
        cursor.close()
        return d
    
    def check_badge(self, query, name, mybadges):
        v = self.get_value(query)
        check_state = v[0]
        in_badge = self.badges[name] in mybadges
        # print str(check_state) + ' <=> ' + str(in_badge) 
        if check_state == in_badge:
            print '.',
            return True
        else:
            print name + ' ERROR'
            return False
            
    def check(self, value, name, mybadges):
        in_badge = self.badges[name] in mybadges
        if value == in_badge:
            print '.',
            return True    
        else:
            name +' ERROR '
            return False

    
    def handle(self, *args, **options):
        
        manager = UserBadge.objects
        
        badges = manager.get_badges()
        
        #  Index by id
        bb = { }
        for b in badges:
            bb[b.name] = b.id
        badges = bb 
        self.badges = badges
            
        for u in SurveyUser.objects.filter(deleted=False):
            print u.global_id
            news = manager.update_badges(u, fake=True)
            mybadges = news['participant']
            
            query = "select count(*)>0 from pollster_results_intake_vx_2012111222301352755848 where global_id='%s'" % u.global_id
            self.check_badge(query, "loyalty1", mybadges)
            
            query = "select count(*)>0 from pollster_results_intake_v0_2013110716251383837914 where global_id='%s'" % u.global_id
            self.check_badge(query, "loyalty2", mybadges)
            
            query = "select count(*) from pollster_results_intake where global_id='%s'" % u.global_id
            v = self.get_value(query)
            count = v[0]
                    
            self.check(count >= 1, 'is_novice', mybadges)
            self.check(count >= 3, 'is_junior', mybadges)
            self.check(count >= 6, 'is_senior', mybadges)
            self.check(count >= 10, 'is_gold', mybadges)
            self.check(count >= 20, 'is_platinum', mybadges)
            print ''
            
        
                
            
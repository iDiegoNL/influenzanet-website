from django.core.management.base import BaseCommand

from django.conf import settings
from apps.survey.models import SurveyUser
from django.core.exceptions import ImproperlyConfigured
from apps.common.db import get_cursor, quote_query
from apps.grippenet.models import Participation

class Command(BaseCommand):
    help = 'Update participation from historical tables'
    
    def handle(self, *args, **options):
        
        try:
            historical = getattr(settings, 'HISTORICAL_TABLES')
        except:
            raise ImproperlyConfigured("Unable to find HISTORICAL_TABLES in settings")
        
        cursor = get_cursor()
        
        participants = {}
        
        for h in historical.items():
            season = int(h[0])
            tables = h[1]
            print "Compute season " + str(season) + "  in " + tables['intake']
            query = quote_query("select min({{timestamp}}),max({{timestamp}}), su.id survey_user_id from " + tables['intake'] + " i left join survey_surveyuser su on su.global_id=i.global_id group by survey_user_id")
            cursor.execute(query)
            rr = cursor.fetchall()
            for r in rr:
                suid = r[2]
                min = r[0]
                max = r[1]
                if suid in participants:
                    p = participants[suid]
                else:
                    p = {'min':None, 'max':None}
                if p['min'] is None or p['min'] > season:
                    p['min'] = season
                if p['max'] is None or p['max'] < season:
                    p['max'] = season
                participants[suid] = p    
        
        for (suid, p) in participants.items():
            try:
                part = Participation.objects.get(survey_user_id=suid)
            except Participation.DoesNotExist:
                part = Participation()
                part.survey_user_id = suid
            part.first_season = p.min
            part.last_season = p.max
            part.save()
        
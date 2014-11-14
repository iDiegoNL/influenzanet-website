from django.db import models

from apps.survey.models import SurveyUser

class PregnantCohort(models.Model):
    survey_user = models.ForeignKey(SurveyUser)
    date_created = models.DateField(auto_now=True)
    active = models.BooleanField(default=True)
    change_channel = models.BooleanField(default=True)
    
class Participation(models.Model):
    survey_user = models.ForeignKey(SurveyUser)
    first_season = models.IntegerField()
    last_season = models.IntegerField()

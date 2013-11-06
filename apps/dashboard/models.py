from django.db import models
from django.contrib.auth.models import User
from apps.survey.models import SurveyUser

#class Badge(models.Model):
#    
#    def __init__(self, name, datasource, updatable):
#        self.name = name
#        self.datasource = datasource
#        self.updatable = updatable
#    
#    def is_updatable(self):
#        return self.updatable
#    
#    def update(self, provider):
#        pass
#    
#class UserBadge(models.Model):
#    user = models.ForeignKey(User)
#    person = models.ForeignKey(SurveyUser, blank=True, Null=True)
#    date = models.DateField()

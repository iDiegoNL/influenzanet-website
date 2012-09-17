from django.db import models

from apps.survey.models import SurveyUser

# Cohort is a group of user

class Cohort(models.Model):
    title = models.CharField(max_length=60)

# Register a user in a given cohort
class CohortUser(models.Model):
    user = models.ForeignKey(SurveyUser, unique=True)
    cohort = models.ForeignKey(Cohort, unique=True)

# A token enables users to register in a given cohort (with a voucher for example).
# Once used you cannot know which user has used which token 
class Token(models.Model):
    cohort = models.ForeignKey(Cohort)
    token = models.CharField(max_length=30, unique=True)
    usage_left = models.IntegerField(min=1, null=True, blank=True)
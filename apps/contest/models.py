from django.db import models
from django.contrib.auth.models import User
from cms.models import CMSPlugin

class ContestPlugin(CMSPlugin):
    title = models.CharField(max_length=255)

class Prediction(models.Model):
    user = models.ForeignKey(User)
    date = models.DateTimeField(auto_now_add=True)

class Week(models.Model):
    prediction = models.ForeignKey(Prediction)
    number = models.IntegerField()
    value = models.CharField(max_length=6, null=True)

    class Meta:
        ordering = ('number',)

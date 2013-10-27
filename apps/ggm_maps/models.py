from django.db import models
from django.db import models
from django.contrib.auth.models import User
from cms.models import CMSPlugin

class GGMMapsPlugin(CMSPlugin):
    title = models.CharField(max_length=255)


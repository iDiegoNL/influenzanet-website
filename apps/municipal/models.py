# -*- coding: utf-8 -*-

from django.db import models

class MunicipalCodes(models.Model):
    zip = models.CharField(max_length=6)
    code = models.CharField(max_length=6)
    title = models.CharField(max_length=60)
    
    class Meta:
        db_table = 'municipal_codes'
    
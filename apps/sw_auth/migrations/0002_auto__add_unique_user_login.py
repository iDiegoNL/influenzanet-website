# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding unique constraint on 'EpiworkUser', fields ['user']
        db.create_unique('sw_auth_epiworkuser', ['user'])

        # Adding unique constraint on 'EpiworkUser', fields ['login']
        db.create_unique('sw_auth_epiworkuser', ['login'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'EpiworkUser', fields ['login']
        db.delete_unique('sw_auth_epiworkuser', ['login'])

        # Removing unique constraint on 'EpiworkUser', fields ['user']
        db.delete_unique('sw_auth_epiworkuser', ['user'])


    models = {
        'sw_auth.epiworkuser': {
            'Meta': {'object_name': 'EpiworkUser'},
            'email': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.BigIntegerField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'login': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'token_activate': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'token_password': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'user': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        }
    }

    complete_apps = ['sw_auth']

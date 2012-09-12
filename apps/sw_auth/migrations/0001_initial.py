# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'EpiworkUser'
        db.create_table('sw_auth_epiworkuser', (
            ('id', self.gf('django.db.models.fields.BigIntegerField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('login', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('token_password', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('token_activate', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('sw_auth', ['EpiworkUser'])


    def backwards(self, orm):
        
        # Deleting model 'EpiworkUser'
        db.delete_table('sw_auth_epiworkuser')


    models = {
        'sw_auth.epiworkuser': {
            'Meta': {'object_name': 'EpiworkUser'},
            'email': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.BigIntegerField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'login': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'token_activate': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'token_password': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'user': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['sw_auth']

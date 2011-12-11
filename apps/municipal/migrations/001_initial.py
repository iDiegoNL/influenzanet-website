# encoding: utf-8

from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'municipalities'
        db.create_table('municipal_codes', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('zip', self.gf('django.db.models.fields.CharField')(max_length=6)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=6)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=60)),
        ))
        db.send_create_signal('municipal', ['MunicipalCodes'])


    def backwards(self, orm):
        
        # Deleting model 'SiteSettings'
        db.delete_table('municipal_codes')


    models = {
        'municipal.codes': {
            'Meta': {'object_name': 'MunicipalCodes'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'zip': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
        }
    }

    complete_apps = ['municipal']

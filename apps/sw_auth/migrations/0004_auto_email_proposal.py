# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'EpiworkUser.email_proposal'
        db.add_column('sw_auth_epiworkuser', 'email_proposal', self.gf('django.db.models.fields.CharField')(max_length=255, null=True), keep_default=False)

        # Adding field 'EpiworkUser.token_email'
        db.add_column('sw_auth_epiworkuser', 'token_email', self.gf('django.db.models.fields.CharField')(max_length=40, null=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'EpiworkUser.email_proposal'
        db.delete_column('sw_auth_epiworkuser', 'email_proposal')

        # Deleting field 'EpiworkUser.token_email'
        db.delete_column('sw_auth_epiworkuser', 'token_email')


    models = {
        'sw_auth.anonymizelog': {
            'Meta': {'object_name': 'AnonymizeLog'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'event': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sw_auth.EpiworkUser']"})
        },
        'sw_auth.epiworkuser': {
            'Meta': {'object_name': 'EpiworkUser'},
            'anonymize_warn': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'email_proposal': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'id': ('django.db.models.fields.BigIntegerField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'login': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'token_activate': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'token_email': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True'}),
            'token_password': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'user': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'sw_auth.logintoken': {
            'Meta': {'object_name': 'LoginToken'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'expires': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '40'}),
            'next': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'usage_left': ('django.db.models.fields.IntegerField', [], {'default': '1', 'null': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sw_auth.EpiworkUser']"})
        }
    }

    complete_apps = ['sw_auth']

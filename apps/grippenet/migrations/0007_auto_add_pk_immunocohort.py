# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'ImmunoCohort.id'
        db.delete_column('grippenet_immunocohort', 'id')

        # Changing field 'ImmunoCohort.survey_user'
        db.alter_column('grippenet_immunocohort', 'survey_user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['survey.SurveyUser'], unique=True, primary_key=True))

        # Adding unique constraint on 'ImmunoCohort', fields ['survey_user']
        db.create_unique('grippenet_immunocohort', ['survey_user_id'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'ImmunoCohort', fields ['survey_user']
        db.delete_unique('grippenet_immunocohort', ['survey_user_id'])

        # User chose to not deal with backwards NULL issues for 'ImmunoCohort.id'
        raise RuntimeError("Cannot reverse this migration. 'ImmunoCohort.id' and its values cannot be restored.")

        # Changing field 'ImmunoCohort.survey_user'
        db.alter_column('grippenet_immunocohort', 'survey_user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['survey.SurveyUser']))


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'grippenet.immunocohort': {
            'Meta': {'object_name': 'ImmunoCohort'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'change_channel': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'date_created': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'survey_user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['survey.SurveyUser']", 'unique': 'True', 'primary_key': 'True'})
        },
        'grippenet.participation': {
            'Meta': {'object_name': 'Participation'},
            'first_season': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_season': ('django.db.models.fields.IntegerField', [], {}),
            'survey_user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['survey.SurveyUser']"})
        },
        'grippenet.pregnantcohort': {
            'Meta': {'object_name': 'PregnantCohort'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'change_channel': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'date_created': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_reminder': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reminder_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'survey_user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['survey.SurveyUser']"})
        },
        'survey.surveyuser': {
            'Meta': {'object_name': 'SurveyUser'},
            'avatar': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'global_id': ('django.db.models.fields.CharField', [], {'default': "'9b903905-f478-4505-851c-f6fa05063e0f'", 'unique': 'True', 'max_length': '36'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_participation_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True'})
        }
    }

    complete_apps = ['grippenet']

# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'LocalProfile'
        db.delete_table('survey_localprofile')

        # Deleting model 'ProfileSendQueue'
        db.delete_table('survey_profilesendqueue')

        # Deleting model 'LastResponse'
        db.delete_table('survey_lastresponse')

        # Deleting model 'Profile'
        db.delete_table('survey_profile')

        # Deleting model 'LocalFluSurvey'
        db.delete_table('survey_localflusurvey')

        # Deleting model 'LocalResponse'
        db.delete_table('survey_localresponse')

        # Deleting model 'Survey'
        db.delete_table('survey_survey')

        # Deleting model 'ResponseSendQueue'
        db.delete_table('survey_responsesendqueue')

        # Deleting model 'Participation'
        db.delete_table('survey_participation')

        # Deleting field 'SurveyUser.last_participation'
        db.delete_column('survey_surveyuser', 'last_participation_id')


    def backwards(self, orm):
        
        # Adding model 'LocalProfile'
        db.create_table('survey_localprofile', (
            ('a_vaccine_prev_swine', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('a_vaccine_current', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('a_smoker', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('region', self.gf('django.db.models.fields.CharField')(max_length=30, null=True)),
            ('a_family', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('a_vaccine_prev_seasonal', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('sq_date_last', self.gf('django.db.models.fields.DateField')(null=True)),
            ('sq_date_first', self.gf('django.db.models.fields.DateField')(null=True)),
            ('birth_date', self.gf('django.db.models.fields.DateField')()),
            ('surveyuser', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['survey.SurveyUser'], unique=True)),
            ('sq_num_season', self.gf('django.db.models.fields.SmallIntegerField')(null=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sq_num_total', self.gf('django.db.models.fields.SmallIntegerField')(null=True)),
            ('zip_code', self.gf('django.db.models.fields.CharField')(max_length=5)),
        ))
        db.send_create_signal('survey', ['LocalProfile'])

        # Adding model 'ProfileSendQueue'
        db.create_table('survey_profilesendqueue', (
            ('user_id', self.gf('django.db.models.fields.CharField')(max_length=36)),
            ('answers', self.gf('django.db.models.fields.TextField')()),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['survey.SurveyUser'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
            ('survey_id', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('survey', ['ProfileSendQueue'])

        # Adding model 'LastResponse'
        db.create_table('survey_lastresponse', (
            ('data', self.gf('django.db.models.fields.TextField')(default=None, null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('participation', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['survey.Participation'], null=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['survey.SurveyUser'], unique=True)),
        ))
        db.send_create_signal('survey', ['LastResponse'])

        # Adding model 'Profile'
        db.create_table('survey_profile', (
            ('updated', self.gf('django.db.models.fields.DateTimeField')(default=None, null=True)),
            ('survey', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['survey.Survey'], null=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['survey.SurveyUser'], unique=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=None, null=True)),
            ('valid', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('data', self.gf('django.db.models.fields.TextField')(default=None, null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('survey', ['Profile'])

        # Adding model 'LocalFluSurvey'
        db.create_table('survey_localflusurvey', (
            ('status', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
            ('surveyuser', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['survey.SurveyUser'])),
            ('survey_id', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('data', self.gf('django.db.models.fields.TextField')()),
            ('age_user', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('survey', ['LocalFluSurvey'])

        # Adding model 'LocalResponse'
        db.create_table('survey_localresponse', (
            ('user_id', self.gf('django.db.models.fields.CharField')(max_length=36)),
            ('answers', self.gf('django.db.models.fields.TextField')()),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
            ('survey_id', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('survey', ['LocalResponse'])

        # Adding model 'Survey'
        db.create_table('survey_survey', (
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('specification', self.gf('django.db.models.fields.TextField')()),
            ('survey_id', self.gf('django.db.models.fields.CharField')(max_length=50, unique=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('survey', ['Survey'])

        # Adding model 'ResponseSendQueue'
        db.create_table('survey_responsesendqueue', (
            ('user_id', self.gf('django.db.models.fields.CharField')(max_length=36)),
            ('answers', self.gf('django.db.models.fields.TextField')()),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('survey_id', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('participation', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['survey.Participation'])),
        ))
        db.send_create_signal('survey', ['ResponseSendQueue'])

        # Adding model 'Participation'
        db.create_table('survey_participation', (
            ('epidb_id', self.gf('django.db.models.fields.CharField')(max_length=36, null=True)),
            ('survey', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['survey.Survey'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['survey.SurveyUser'])),
            ('previous_participation', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['survey.Participation'], null=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('previous_participation_date', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('survey', ['Participation'])

        # Adding field 'SurveyUser.last_participation'
        db.add_column('survey_surveyuser', 'last_participation', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['survey.Participation'], null=True), keep_default=False)


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
        'survey.surveyuser': {
            'Meta': {'object_name': 'SurveyUser'},
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'global_id': ('django.db.models.fields.CharField', [], {'default': "'f5b9ff63-4c7c-4662-8ca2-46ab850ecc4b'", 'unique': 'True', 'max_length': '36'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_participation_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True'})
        }
    }

    complete_apps = ['survey']

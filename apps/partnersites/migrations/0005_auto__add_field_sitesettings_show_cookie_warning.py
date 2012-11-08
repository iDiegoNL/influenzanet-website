# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'SiteSettings.show_cookie_warning'
        db.add_column('partnersites_sitesettings', 'show_cookie_warning',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'SiteSettings.show_cookie_warning'
        db.delete_column('partnersites_sitesettings', 'show_cookie_warning')


    models = {
        'partnersites.sitesettings': {
            'Meta': {'object_name': 'SiteSettings'},
            'contact_form_recipient': ('django.db.models.fields.EmailField', [], {'default': "'webdev@grotegriepmeting.nl'", 'max_length': '75', 'blank': 'True'}),
            'footer': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'light_color': ('django.db.models.fields.CharField', [], {'default': "'ce2626'", 'max_length': '6'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'show_cookie_warning': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'site': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['sites.Site']", 'unique': 'True'})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['partnersites']
# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'List.secret_id'
        db.delete_column('lists_list', 'secret_id')

        # Adding field 'List.access_code'
        db.add_column('lists_list', 'access_code', self.gf('django.db.models.fields.CharField')(default='nosecret', max_length=8), keep_default=False)

        # Adding field 'List.admin_code'
        db.add_column('lists_list', 'admin_code', self.gf('django.db.models.fields.CharField')(default='nosecret', max_length=8), keep_default=False)

        # Adding field 'List.published'
        db.add_column('lists_list', 'published', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True), keep_default=False)

        # Adding field 'UGC.censored'
        db.add_column('lists_ugc', 'censored', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Adding field 'List.secret_id'
        db.add_column('lists_list', 'secret_id', self.gf('django.db.models.fields.CharField')(default='notasecret', max_length=10), keep_default=False)

        # Deleting field 'List.access_code'
        db.delete_column('lists_list', 'access_code')

        # Deleting field 'List.admin_code'
        db.delete_column('lists_list', 'admin_code')

        # Deleting field 'List.published'
        db.delete_column('lists_list', 'published')

        # Deleting field 'UGC.censored'
        db.delete_column('lists_ugc', 'censored')


    models = {
        'lists.entry': {
            'Meta': {'object_name': 'Entry', '_ormbases': ['lists.UGC']},
            'description': ('django.db.models.fields.TextField', [], {}),
            'list': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lists.List']"}),
            'rating_score': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'rating_votes': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'ugc_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['lists.UGC']", 'unique': 'True', 'primary_key': 'True'})
        },
        'lists.list': {
            'Meta': {'object_name': 'List', '_ormbases': ['lists.UGC']},
            'access_code': ('django.db.models.fields.CharField', [], {'default': "'nosecret'", 'max_length': '8'}),
            'admin_code': ('django.db.models.fields.CharField', [], {'default': "'nosecret'", 'max_length': '8'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'ugc_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['lists.UGC']", 'unique': 'True', 'primary_key': 'True'}),
            'views': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        'lists.ugc': {
            'Meta': {'object_name': 'UGC', '_ormbases': ['lists.user_action']},
            'censored': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'nickname': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'user_action_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['lists.user_action']", 'unique': 'True', 'primary_key': 'True'})
        },
        'lists.user_action': {
            'Meta': {'object_name': 'user_action'},
            'absolute_uri': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'is_ajax': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'is_secure': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'referer': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'user_agent': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['lists']

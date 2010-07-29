# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'user_action'
        db.create_table('lists_user_action', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
            ('referer', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('user_agent', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('ip', self.gf('django.db.models.fields.IPAddressField')(max_length=15, blank=True)),
            ('absolute_uri', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('is_secure', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('is_ajax', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
        ))
        db.send_create_signal('lists', ['user_action'])

        # Adding model 'UGC'
        db.create_table('lists_ugc', (
            ('user_action_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['lists.user_action'], unique=True, primary_key=True)),
            ('nickname', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
        ))
        db.send_create_signal('lists', ['UGC'])

        # Deleting field 'List.id'
        db.delete_column('lists_list', 'id')

        # Adding field 'List.ugc_ptr'
        db.add_column('lists_list', 'ugc_ptr', self.gf('django.db.models.fields.related.OneToOneField')(default=0, to=orm['lists.UGC'], unique=True, primary_key=True), keep_default=False)

        # Adding field 'List.views'
        db.add_column('lists_list', 'views', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)

        # Deleting field 'Entry.id'
        db.delete_column('lists_entry', 'id')

        # Adding field 'Entry.ugc_ptr'
        db.add_column('lists_entry', 'ugc_ptr', self.gf('django.db.models.fields.related.OneToOneField')(default=0, to=orm['lists.UGC'], unique=True, primary_key=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting model 'user_action'
        db.delete_table('lists_user_action')

        # Deleting model 'UGC'
        db.delete_table('lists_ugc')

        # Adding field 'List.id'
        db.add_column('lists_list', 'id', self.gf('django.db.models.fields.AutoField')(default=0, primary_key=True), keep_default=False)

        # Deleting field 'List.ugc_ptr'
        db.delete_column('lists_list', 'ugc_ptr_id')

        # Deleting field 'List.views'
        db.delete_column('lists_list', 'views')

        # Adding field 'Entry.id'
        db.add_column('lists_entry', 'id', self.gf('django.db.models.fields.AutoField')(default=0, primary_key=True), keep_default=False)

        # Deleting field 'Entry.ugc_ptr'
        db.delete_column('lists_entry', 'ugc_ptr_id')


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
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'secret_id': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'ugc_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['lists.UGC']", 'unique': 'True', 'primary_key': 'True'}),
            'views': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'lists.ugc': {
            'Meta': {'object_name': 'UGC', '_ormbases': ['lists.user_action']},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'nickname': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'user_action_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['lists.user_action']", 'unique': 'True', 'primary_key': 'True'})
        },
        'lists.user_action': {
            'Meta': {'object_name': 'user_action'},
            'absolute_uri': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'blank': 'True'}),
            'is_ajax': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'is_secure': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'referer': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'user_agent': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'})
        }
    }

    complete_apps = ['lists']

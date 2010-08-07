# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'Image'
        db.delete_table('lists_image')

        # Deleting model 'user_action'
        db.delete_table('lists_user_action')

        # Adding model 'UserAction'
        db.create_table('lists_useraction', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
            ('referer', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('user_agent', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('ip', self.gf('django.db.models.fields.IPAddressField')(max_length=15, null=True, blank=True)),
            ('absolute_uri', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('is_secure', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('is_ajax', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
        ))
        db.send_create_signal('lists', ['UserAction'])

        # Adding model 'UploadedImage'
        db.create_table('lists_uploadedimage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('source_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('alt', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('original_image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('num_views', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
        ))
        db.send_create_signal('lists', ['UploadedImage'])

        # Changing field 'Entry.description'
        db.alter_column('lists_entry', 'description', self.gf('django.db.models.fields.TextField')(blank=True))

        # Changing field 'Entry.image'
        db.alter_column('lists_entry', 'image_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lists.UploadedImage'], null=True, blank=True))

        # Deleting field 'UGC.user_action_ptr'
        db.delete_column('lists_ugc', 'user_action_ptr_id')

        # Adding field 'UGC.useraction_ptr'
        db.add_column('lists_ugc', 'useraction_ptr', self.gf('django.db.models.fields.related.OneToOneField')(default=1, to=orm['lists.UserAction'], unique=True, primary_key=True), keep_default=False)


    def backwards(self, orm):
        
        # Adding model 'Image'
        db.create_table('lists_image', (
            ('original_image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('num_views', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('source', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('lists', ['Image'])

        # Adding model 'user_action'
        db.create_table('lists_user_action', (
            ('is_secure', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('referer', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('user_agent', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('is_ajax', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('ip', self.gf('django.db.models.fields.IPAddressField')(max_length=15, null=True, blank=True)),
            ('absolute_uri', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('modified', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('lists', ['user_action'])

        # Deleting model 'UserAction'
        db.delete_table('lists_useraction')

        # Deleting model 'UploadedImage'
        db.delete_table('lists_uploadedimage')

        # Changing field 'Entry.description'
        db.alter_column('lists_entry', 'description', self.gf('django.db.models.fields.TextField')())

        # Changing field 'Entry.image'
        db.alter_column('lists_entry', 'image_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lists.Image'], null=True, blank=True))

        # Adding field 'UGC.user_action_ptr'
        db.add_column('lists_ugc', 'user_action_ptr', self.gf('django.db.models.fields.related.OneToOneField')(default=1, to=orm['lists.user_action'], unique=True, primary_key=True), keep_default=False)

        # Deleting field 'UGC.useraction_ptr'
        db.delete_column('lists_ugc', 'useraction_ptr_id')


    models = {
        'lists.entry': {
            'Meta': {'object_name': 'Entry', '_ormbases': ['lists.UGC']},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'embed_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'image': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lists.UploadedImage']", 'null': 'True', 'blank': 'True'}),
            'list': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lists.List']"}),
            'rating_score': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'rating_votes': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'ugc_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['lists.UGC']", 'unique': 'True', 'primary_key': 'True'})
        },
        'lists.list': {
            'Meta': {'object_name': 'List', '_ormbases': ['lists.UGC']},
            'access_code': ('django.db.models.fields.CharField', [], {'default': "'t2jfavos'", 'max_length': '8'}),
            'admin_code': ('django.db.models.fields.CharField', [], {'default': "'gtp7ml9z'", 'max_length': '8'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'ugc_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['lists.UGC']", 'unique': 'True', 'primary_key': 'True'}),
            'views': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        'lists.ugc': {
            'Meta': {'object_name': 'UGC', '_ormbases': ['lists.UserAction']},
            'censored': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'nickname': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'useraction_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['lists.UserAction']", 'unique': 'True', 'primary_key': 'True'})
        },
        'lists.uploadedimage': {
            'Meta': {'object_name': 'UploadedImage'},
            'alt': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'num_views': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'original_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'source_url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'lists.useraction': {
            'Meta': {'object_name': 'UserAction'},
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

# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Image'
        db.create_table('lists_image', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('source', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('original_image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('num_views', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
        ))
        db.send_create_signal('lists', ['Image'])

        # Adding field 'Entry.image'
        db.add_column('lists_entry', 'image', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lists.Image'], null=True, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting model 'Image'
        db.delete_table('lists_image')

        # Deleting field 'Entry.image'
        db.delete_column('lists_entry', 'image_id')


    models = {
        'lists.entry': {
            'Meta': {'object_name': 'Entry', '_ormbases': ['lists.UGC']},
            'description': ('django.db.models.fields.TextField', [], {}),
            'image': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lists.Image']", 'null': 'True', 'blank': 'True'}),
            'list': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lists.List']"}),
            'oembed': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'rating_score': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'rating_votes': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'ugc_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['lists.UGC']", 'unique': 'True', 'primary_key': 'True'})
        },
        'lists.image': {
            'Meta': {'object_name': 'Image'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'num_views': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'original_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'source': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'lists.list': {
            'Meta': {'object_name': 'List', '_ormbases': ['lists.UGC']},
            'access_code': ('django.db.models.fields.CharField', [], {'default': "'wwj9crk0'", 'max_length': '8'}),
            'admin_code': ('django.db.models.fields.CharField', [], {'default': "'w6p9it9o'", 'max_length': '8'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
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

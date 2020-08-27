# Generated by Django 3.0.8 on 2020-08-27 07:21

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import jsonfield.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('batch', '0001_initial'),
        ('auth_user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Upload',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('file_id', models.CharField(db_index=True, max_length=255)),
                ('name', models.CharField(db_index=True, max_length=255)),
                ('valid', models.BooleanField(default=False)),
                ('content_type', models.CharField(blank=True, max_length=250, null=True)),
                ('path', models.CharField(db_index=True, max_length=255)),
                ('date_created', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('uploaded_chunks', jsonfield.fields.JSONField(default=dict)),
                ('uploaded_size', models.BigIntegerField(null=True)),
                ('batch', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='upload', to='batch.Batch')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='auth_user.User')),
            ],
            options={
                'db_table': 'app_upload',
                'ordering': ['-date_created'],
                'unique_together': {('user', 'batch', 'file_id')},
            },
        ),
    ]

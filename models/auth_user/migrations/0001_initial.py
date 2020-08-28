# Generated by Django 3.0.8 on 2020-08-23 11:16

import django.contrib.auth.models
from django.db import migrations
from django.contrib.auth.hashers import make_password

def load_initial_user(apps, schema_editor):
    """
    load initial user
    """
    User = apps.get_model("auth_user", "User")
    user, _ = User.objects.get_or_create(
        email='testuser@venn.bio',
        username='testuser')
    user.is_superuser = True
    user.is_staff = True
    user.password = make_password('1234')
    user.save()

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.RunPython(load_initial_user),
    ]

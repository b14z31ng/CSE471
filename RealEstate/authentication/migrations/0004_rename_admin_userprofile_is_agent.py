# Generated by Django 5.0.2 on 2024-03-22 18:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_userprofile_admin'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='admin',
            new_name='is_agent',
        ),
    ]

# Generated by Django 5.0.2 on 2024-02-29 21:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
        ('property', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='allproperty',
            old_name='type',
            new_name='property_type',
        ),
        migrations.AddField(
            model_name='allproperty',
            name='Media',
            field=models.ImageField(default=None, upload_to='pics'),
        ),
        migrations.AlterField(
            model_name='allproperty',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='properties', to='authentication.userprofile'),
        ),
    ]

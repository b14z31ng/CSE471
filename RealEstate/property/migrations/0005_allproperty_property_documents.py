# Generated by Django 5.0.2 on 2024-03-22 20:28

import django.core.validators
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0004_remove_allproperty_district_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='allproperty',
            name='Property_Documents',
            field=models.FileField(default=django.utils.timezone.now, upload_to='property_documents/', validators=[django.core.validators.FileExtensionValidator(['pdf'])]),
            preserve_default=False,
        ),
    ]

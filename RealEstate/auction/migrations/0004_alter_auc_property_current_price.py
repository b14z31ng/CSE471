# Generated by Django 5.0.2 on 2024-04-15 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0003_auc_property_approval_by_agent_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auc_property',
            name='current_price',
            field=models.PositiveIntegerField(default=models.PositiveIntegerField(default=1)),
        ),
    ]

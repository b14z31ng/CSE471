# Generated by Django 5.0.2 on 2024-03-20 19:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Agents', '0002_agent_delete_agentprofile'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Agent',
        ),
    ]

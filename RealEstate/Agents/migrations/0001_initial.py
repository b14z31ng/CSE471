# Generated by Django 5.0.2 on 2024-04-02 13:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authentication', '0001_initial'),
        ('property', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_slot', models.DateTimeField()),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=20)),
                ('agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.userprofile')),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='property.allproperty')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings_as_seller', to='authentication.userprofile')),
            ],
        ),
    ]

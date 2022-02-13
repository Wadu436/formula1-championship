# Generated by Django 4.0.2 on 2022-02-13 22:52

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leaderboard', '0040_championshipdriver_penalty_points_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='raceentry',
            name='pit_stops',
        ),
        migrations.AlterField(
            model_name='raceentry',
            name='qualifying_position',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1)], verbose_name='Qualifying Position'),
        ),
    ]

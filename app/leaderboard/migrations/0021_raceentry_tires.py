# Generated by Django 4.0 on 2021-12-23 00:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leaderboard', '0020_remove_raceentry_raceentry_dna_notnull_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='raceentry',
            name='tires',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
    ]

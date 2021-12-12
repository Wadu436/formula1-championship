# Generated by Django 4.0rc1 on 2021-12-12 01:57

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('leaderboard', '0005_remove_raceentry_raceentry_dna_notnull_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='championship',
            options={'get_latest_by': 'start_date'},
        ),
        migrations.AddField(
            model_name='championship',
            name='start_date',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]

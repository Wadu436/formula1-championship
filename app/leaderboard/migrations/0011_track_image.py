# Generated by Django 4.0 on 2021-12-19 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leaderboard', '0010_race_length_track_full_laps_track_long_laps_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='track',
            name='image',
            field=models.ImageField(default='', upload_to=''),
            preserve_default=False,
        ),
    ]
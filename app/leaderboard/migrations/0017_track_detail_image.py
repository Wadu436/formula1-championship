# Generated by Django 4.0 on 2021-12-20 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leaderboard', '0016_rename_image_track_overview_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='track',
            name='detail_image',
            field=models.ImageField(blank=True, default=None, null=True, upload_to=''),
        ),
    ]
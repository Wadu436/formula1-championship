# Generated by Django 4.0 on 2021-12-19 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leaderboard', '0013_alter_track_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='track',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]

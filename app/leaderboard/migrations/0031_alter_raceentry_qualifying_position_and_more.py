# Generated by Django 4.0 on 2021-12-26 15:40

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('leaderboard', '0030_alter_raceentry_best_lap_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='raceentry',
            name='qualifying_position',
            field=models.IntegerField(blank=True, validators=[django.core.validators.MinValueValidator(1)], verbose_name='Qualifying Position'),
        ),
        migrations.CreateModel(
            name='ConstructorMultiplier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('multiplier', models.FloatField()),
                ('championship', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='multipliers', to='leaderboard.championship')),
                ('constructor', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='multipliers', to='leaderboard.team')),
            ],
        ),
    ]
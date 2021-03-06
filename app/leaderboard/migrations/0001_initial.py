# Generated by Django 4.0rc1 on 2021-12-05 00:47

import colorfield.fields
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('nickname', models.CharField(blank=True, max_length=64, null=True)),
                ('country', django_countries.fields.CountryField(max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Race',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tournament_order', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('date_time', models.DateTimeField()),
                ('finished', models.BooleanField(default=False)),
                ('wet_race', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('color', colorfield.fields.ColorField(default='#FF0000', max_length=18)),
                ('country', django_countries.fields.CountryField(max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Tournament',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=64)),
                ('name', models.CharField(blank=True, max_length=64, null=True)),
                ('abbreviation', models.CharField(max_length=8)),
                ('country', django_countries.fields.CountryField(max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='RaceEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dna', models.BooleanField(default=False, verbose_name='Did Not Attend')),
                ('qualifying_position', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1)], verbose_name='Qualifying Position')),
                ('grid_penalty', models.PositiveIntegerField(default=0)),
                ('finish_position', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1)])),
                ('full_time', models.DurationField(blank=True, null=True, verbose_name='Full Race Time')),
                ('best_lap_time', models.DurationField(blank=True, null=True)),
                ('pit_stops', models.PositiveIntegerField(blank=True, default=1, null=True)),
                ('dnf', models.BooleanField(blank=True, default=False, null=True, verbose_name='Did Not Finish')),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='leaderboard.driver')),
                ('race', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='leaderboard.race')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='leaderboard.team')),
            ],
        ),
        migrations.AddField(
            model_name='race',
            name='tournament',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='leaderboard.tournament'),
        ),
        migrations.AddField(
            model_name='race',
            name='track',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='leaderboard.track'),
        ),
        migrations.AddField(
            model_name='driver',
            name='team',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='leaderboard.team'),
        ),
        migrations.AddConstraint(
            model_name='raceentry',
            constraint=models.UniqueConstraint(fields=('race', 'driver'), name='raceentry_unique_driver_race'),
        ),
        migrations.AddConstraint(
            model_name='raceentry',
            constraint=models.CheckConstraint(check=models.Q(('dna', True)), name='raceentry_dna_notnull'),
        ),
        migrations.AddConstraint(
            model_name='race',
            constraint=models.UniqueConstraint(fields=('tournament_order', 'tournament'), name='race_unique_tournament_order'),
        ),
    ]

# Generated by Django 4.0 on 2021-12-22 22:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('leaderboard', '0018_alter_race_track'),
    ]

    operations = [
        migrations.CreateModel(
            name='DNAEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.RemoveConstraint(
            model_name='raceentry',
            name='raceentry_dna_notnull',
        ),
        migrations.RemoveField(
            model_name='raceentry',
            name='dna',
        ),
        migrations.AddField(
            model_name='raceentry',
            name='bot',
            field=models.BooleanField(default=False, verbose_name='Is Bot'),
        ),
        migrations.AlterField(
            model_name='raceentry',
            name='driver',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='race_entries', to='leaderboard.driver'),
        ),
        migrations.AlterField(
            model_name='raceentry',
            name='team',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='race_entries', to='leaderboard.team'),
        ),
        migrations.AddConstraint(
            model_name='raceentry',
            constraint=models.CheckConstraint(check=models.Q(models.Q(('best_lap_time__isnull', False), ('bot', True), ('finish_position__isnull', False)), models.Q(('best_lap_time__isnull', False), ('bot', False), ('dnf__isnull', False), ('driver__isnull', False), ('finish_position__isnull', False), ('grid_penalty__isnull', False), ('pit_stops__isnull', False), ('qualifying_position__isnull', False), ('team__isnull', False)), _connector='OR'), name='raceentry_dna_notnull'),
        ),
        migrations.AddField(
            model_name='dnaentry',
            name='driver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='dna_entries', to='leaderboard.driver'),
        ),
        migrations.AddField(
            model_name='dnaentry',
            name='race',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dna_entries', to='leaderboard.race'),
        ),
        migrations.AddField(
            model_name='dnaentry',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='dna_entries', to='leaderboard.team'),
        ),
    ]

# Generated by Django 4.0.2 on 2022-02-22 16:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('leaderboard', '0043_sprintrace_sprintraceentry_sprintdnaentry_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sprintrace',
            name='championship',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sprint_races', to='leaderboard.championship'),
        ),
        migrations.AlterField(
            model_name='sprintrace',
            name='track',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='sprint_races', to='leaderboard.track'),
        ),
    ]
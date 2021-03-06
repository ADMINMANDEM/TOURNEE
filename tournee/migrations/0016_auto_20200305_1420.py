# Generated by Django 2.2.7 on 2020-03-05 14:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tournee', '0015_auto_20200304_0953'),
    ]

    operations = [
        migrations.CreateModel(
            name='Seed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seed', models.IntegerField(db_column='Seed')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tournee.Team')),
                ('tournament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tournee.Tournament')),
            ],
        ),
        migrations.RemoveField(
            model_name='tournamentresult',
            name='team_id',
        ),
        migrations.RemoveField(
            model_name='tournamentresult',
            name='tournamentid',
        ),
        migrations.DeleteModel(
            name='GameScore',
        ),
        migrations.DeleteModel(
            name='TournamentResult',
        ),
    ]

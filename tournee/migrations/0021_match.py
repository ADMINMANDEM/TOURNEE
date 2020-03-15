# Generated by Django 2.2.7 on 2020-03-10 13:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tournee', '0020_auto_20200310_1056'),
    ]

    operations = [
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(db_column='Score', null=True)),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tournee.Team')),
                ('tournament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tournee.Tournament')),
            ],
        ),
    ]

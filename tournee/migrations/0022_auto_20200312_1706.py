# Generated by Django 2.2.7 on 2020-03-12 17:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tournee', '0021_match'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='seed',
            name='competing',
        ),
        migrations.DeleteModel(
            name='Match',
        ),
    ]

# Generated by Django 2.2.7 on 2020-03-05 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournee', '0017_auto_20200305_1433'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seed',
            name='seed',
            field=models.IntegerField(db_column='Seed', null=True),
        ),
    ]
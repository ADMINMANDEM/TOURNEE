# Generated by Django 2.2.7 on 2020-03-02 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournee', '0004_auto_20200302_1503'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='nationality',
            field=models.CharField(blank=True, db_column='Nationality', max_length=32, null=True),
        ),
    ]

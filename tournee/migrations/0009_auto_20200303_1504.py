# Generated by Django 2.2.7 on 2020-03-03 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournee', '0008_auto_20200303_1455'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membership',
            name='date_joined',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]

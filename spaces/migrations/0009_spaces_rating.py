# Generated by Django 3.2.4 on 2021-06-28 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spaces', '0008_auto_20210628_1154'),
    ]

    operations = [
        migrations.AddField(
            model_name='spaces',
            name='rating',
            field=models.CharField(default='', max_length=4),
        ),
    ]

# Generated by Django 3.2.4 on 2021-06-29 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spaces', '0010_auto_20210629_1207'),
    ]

    operations = [
        migrations.AddField(
            model_name='spaces',
            name='telephone',
            field=models.CharField(default='', max_length=64),
        ),
    ]

# Generated by Django 3.2.4 on 2021-07-06 12:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spaces', '0011_spaces_telephone'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='spaces',
            options={'ordering': ['-created'], 'verbose_name': 'Space', 'verbose_name_plural': 'Spaces'},
        ),
    ]
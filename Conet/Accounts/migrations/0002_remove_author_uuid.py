# Generated by Django 2.1.5 on 2019-03-04 19:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='author',
            name='uuid',
        ),
    ]

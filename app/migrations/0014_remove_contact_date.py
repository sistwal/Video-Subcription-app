# Generated by Django 3.2.6 on 2021-09-13 11:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_contact'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contact',
            name='date',
        ),
    ]

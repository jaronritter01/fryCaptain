# Generated by Django 3.2 on 2021-08-02 16:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('resturant', '0011_auto_20210802_1105'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='user',
        ),
    ]

# Generated by Django 3.2 on 2021-08-02 17:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('resturant', '0015_customer_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='password',
        ),
    ]

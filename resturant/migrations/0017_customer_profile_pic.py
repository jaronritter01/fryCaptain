# Generated by Django 3.2 on 2021-08-02 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resturant', '0016_remove_customer_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]

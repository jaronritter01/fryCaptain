# Generated by Django 3.2 on 2021-08-16 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resturant', '0029_alter_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='menuitem',
            name='fry_type',
            field=models.CharField(blank=True, choices=[('aioli', 'aioli'), ('ketchup', 'ketchup')], max_length=200, null=True),
        ),
    ]

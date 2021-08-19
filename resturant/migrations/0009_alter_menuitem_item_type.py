# Generated by Django 3.2 on 2021-07-14 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resturant', '0008_menuitem_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuitem',
            name='item_type',
            field=models.CharField(choices=[('appetizer', 'appetizer'), ('entree', 'entree'), ('dessert', 'dessert'), ('challenge', 'challenge')], max_length=200, null=True),
        ),
    ]

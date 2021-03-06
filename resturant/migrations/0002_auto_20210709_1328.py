# Generated by Django 3.2 on 2021-07-09 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resturant', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, null=True)),
                ('email', models.CharField(max_length=100, null=True)),
                ('password', models.CharField(max_length=100, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='menuitem',
            name='price',
            field=models.FloatField(null=True),
        ),
    ]

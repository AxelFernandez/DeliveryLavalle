# Generated by Django 3.0.5 on 2020-12-22 01:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20201215_2046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='is_available',
            field=models.BooleanField(default=True),
        ),
    ]

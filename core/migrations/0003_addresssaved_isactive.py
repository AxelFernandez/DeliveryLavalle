# Generated by Django 3.0.5 on 2020-12-09 02:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_firebasetoken'),
    ]

    operations = [
        migrations.AddField(
            model_name='addresssaved',
            name='isActive',
            field=models.BooleanField(default=True, null=True),
        ),
    ]
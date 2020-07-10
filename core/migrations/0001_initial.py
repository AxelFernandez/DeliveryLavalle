# Generated by Django 3.0.5 on 2020-06-06 22:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=150)),
                ('phone', models.CharField(max_length=50)),
                ('available_now', models.CharField(choices=[('SI', 'Si'), ('NO', 'No')], default='Si', max_length=2)),
                ('photo', models.FileField(upload_to='DeliveryLavalle')),
                ('limits', models.CharField(max_length=1000)),
                ('id_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PaymentMethod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=250)),
                ('is_available', models.CharField(choices=[('SI', 'Si'), ('NO', 'No')], default='Si', max_length=2)),
                ('photo', models.FileField(upload_to='DeliveryLavalle')),
                ('id_company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Company')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now=True)),
                ('location', models.FloatField()),
                ('id_company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Company')),
                ('id_state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.State')),
                ('product', models.ManyToManyField(to='core.Products', verbose_name='List to Products to Order')),
            ],
        ),
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=50)),
                ('date', models.DateTimeField(auto_now=True)),
                ('id_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Order')),
                ('id_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

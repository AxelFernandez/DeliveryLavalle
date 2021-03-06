# Generated by Django 3.0.5 on 2020-09-01 03:58

import cloudinary.models
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
            name='AddressSaved',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street', models.CharField(max_length=100)),
                ('number', models.CharField(max_length=100)),
                ('district', models.CharField(max_length=100)),
                ('floor', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('reference', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('location', models.CharField(blank=True, default='', max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(blank=True, max_length=100, null=True)),
                ('photo', models.CharField(max_length=4000)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=150)),
                ('phone', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=50)),
                ('available_now', models.CharField(choices=[('SI', 'Si'), ('NO', 'No')], default='Si', max_length=2)),
                ('photo', cloudinary.models.CloudinaryField(max_length=255, verbose_name='image')),
                ('limits', models.CharField(max_length=1000)),
                ('account_debit', models.FloatField()),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='CompanyCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=150)),
                ('photo', models.CharField(max_length=3000)),
            ],
        ),
        migrations.CreateModel(
            name='DeliveryMethod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=50)),
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
            name='ProductCategories',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=250)),
                ('company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Company')),
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
                ('price', models.IntegerField()),
                ('is_available', models.CharField(choices=[('SI', 'Si'), ('NO', 'No')], default='Si', max_length=2)),
                ('photo', cloudinary.models.CloudinaryField(max_length=255, verbose_name='image')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.ProductCategories')),
                ('id_company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Company')),
            ],
        ),
        migrations.CreateModel(
            name='PaymentService',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_date', models.DateField(auto_now_add=True)),
                ('payment_status', models.CharField(max_length=45)),
                ('mount', models.FloatField()),
                ('transaction_date', models.DateField(null=True)),
                ('description', models.CharField(max_length=45)),
                ('period', models.CharField(max_length=45)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Company')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('retry_in_local', models.BooleanField(default=False)),
                ('total', models.IntegerField()),
                ('address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.AddressSaved')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Client')),
                ('id_company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Company')),
                ('payment_method', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.PaymentMethod')),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.State')),
            ],
        ),
        migrations.CreateModel(
            name='MeLiTransaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('preference_id', models.CharField(max_length=100)),
                ('payment_id', models.CharField(max_length=45)),
                ('payment_status', models.CharField(max_length=45)),
                ('payment_status_detail', models.CharField(max_length=45)),
                ('merchant_order_id', models.CharField(max_length=45)),
                ('processing_mode', models.CharField(max_length=45)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('payment_service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.PaymentService')),
            ],
        ),
        migrations.CreateModel(
            name='MeliLinks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.CharField(max_length=1024)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Order')),
            ],
        ),
        migrations.CreateModel(
            name='DetailOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Products')),
            ],
        ),
        migrations.AddField(
            model_name='company',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.CompanyCategory'),
        ),
        migrations.AddField(
            model_name='company',
            name='delivery_method',
            field=models.ManyToManyField(to='core.DeliveryMethod'),
        ),
        migrations.AddField(
            model_name='company',
            name='id_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='company',
            name='payment_method',
            field=models.ManyToManyField(to='core.PaymentMethod'),
        ),
        migrations.AddField(
            model_name='addresssaved',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Client'),
        ),
    ]

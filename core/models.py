from django.conf import settings
from django.db import models

# Create your models here.




class Company(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=150)
    phone = models.CharField(max_length=50)
    available_now = models.BooleanField(default=True)
    photo = models.FileField(upload_to='DeliveryLavalle')
    id_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Products(models.Model):
    name = models.CharField(max_length=50)
    is_available = models.BooleanField(default=True)
    photo = models.FileField(upload_to='DeliveryLavalle')
    id_company = models.ForeignKey(Company, on_delete=models.CASCADE)


class PaymentMethod(models.Model):
    description = models.CharField(max_length=50)


class State(models.Model):
    description = models.CharField(max_length=50)


class Limits(models.Model):
    limit_NE = models.FloatField()
    limit_NO = models.FloatField()
    limit_SE = models.FloatField()
    limit_SO = models.FloatField()
    company_id = models.ForeignKey(Company,on_delete=models.CASCADE)


class Order(models.Model):
    product = models.ManyToManyField(Products, verbose_name='List to Products to Order')
    id_company = models.ForeignKey(Company,on_delete=models.CASCADE)
    id_state = models.ForeignKey(State,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    location = models.FloatField()


class Chat(models.Model):
    id_order = models.ForeignKey(Order, on_delete=models.CASCADE)
    id_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now=True)

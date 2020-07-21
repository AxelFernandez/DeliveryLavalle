from django.conf import settings
from django.db import models

from core import YES_NO_CHOICES


class Company(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=150)
    phone = models.CharField(max_length=50)
    available_now = models.CharField(max_length=2, choices=YES_NO_CHOICES, default="Si")
    photo = models.FileField(upload_to='DeliveryLavalle')
    id_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    limits = models.CharField(max_length=1000)


class Products(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    is_available = models.CharField(max_length=2, choices=YES_NO_CHOICES, default="Si")
    photo = models.FileField(upload_to='DeliveryLavalle')
    id_company = models.ForeignKey(Company, on_delete=models.CASCADE)




class PaymentMethod(models.Model):
    description = models.CharField(max_length=50)


class State(models.Model):
    description = models.CharField(max_length=50)


class Order(models.Model):
    id_company = models.ForeignKey(Company, on_delete=models.CASCADE)
    id_state = models.ForeignKey(State, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    location = models.CharField(max_length=100)


class DetailOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField()


class Chat(models.Model):
    id_order = models.ForeignKey(Order, on_delete=models.CASCADE)
    id_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now=True)

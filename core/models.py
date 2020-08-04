from django.conf import settings
from django.db import models

from core import YES_NO_CHOICES


class Company(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=150)
    phone = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    available_now = models.CharField(max_length=2, choices=YES_NO_CHOICES, default="Si")
    photo = models.FileField(upload_to='company_storage')
    id_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    limits = models.CharField(max_length=1000)
    account_debit = models.IntegerField()

    def __str__(self):
        return self.name


class Products(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    price = models.IntegerField()
    is_available = models.CharField(max_length=2, choices=YES_NO_CHOICES, default="Si")
    photo = models.FileField(upload_to='products_storage')
    id_company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Client(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    photo = models.FileField(upload_to='client_storage')

    def __str__(self):
        return "{} + ' '+ {}".format(self.user.first_name, self.user.last_name)


class PaymentMethod(models.Model):
    description = models.CharField(max_length=50)

    def __str__(self):
        return self.description


class State(models.Model):
    description = models.CharField(max_length=50)

    def __str__(self):
        return self.description


class Order(models.Model):
    id_company = models.ForeignKey(Company, on_delete=models.CASCADE)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=100)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)
    total = models.IntegerField()


class MeliLinks(models.Model):
    link = models.CharField(max_length=1024)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)


class DetailOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField()


class Chat(models.Model):
    id_order = models.ForeignKey(Order, on_delete=models.CASCADE)
    id_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True)


# Business Rule: this must run every first day in every mount
class PaymentService(models.Model):
    company = models.ForeignKey(Company,on_delete=models.CASCADE)
    payment_date = models.DateField(auto_now_add=True)
    payment_status = models.CharField(max_length=45)
    mount = models.FloatField()
    transaction_date = models.DateField(null=True)
    description = models.CharField(max_length=45)


class MeLiTransaction(models.Model):
    collection_id = models.IntegerField()
    collection_status = models.CharField(max_length=45)
    payment_type = models.CharField(max_length=45)
    merchant_order_id = models.IntegerField()
    preference_id = models.IntegerField()
    payment_service = models.ForeignKey(PaymentService, on_delete=models.CASCADE)


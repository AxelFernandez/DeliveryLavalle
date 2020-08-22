from cloudinary.models import CloudinaryField
from django.conf import settings
from django.db import models
from django_resized import ResizedImageField

from core import YES_NO_CHOICES


class PaymentMethod(models.Model):
    description = models.CharField(max_length=50)

    def __str__(self):
        return self.description


class CompanyCategory(models.Model):
    description = models.CharField(max_length=150)

    def __str__(self):
        return self.description


class Company(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=150)
    phone = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    available_now = models.CharField(max_length=2, choices=YES_NO_CHOICES, default="Si")
    photo = CloudinaryField('image')
    id_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    limits = models.CharField(max_length=1000)
    category = models.ForeignKey(CompanyCategory,on_delete=models.CASCADE)
    account_debit = models.FloatField()
    payment_method = models.ManyToManyField(PaymentMethod)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ProductCategories(models.Model):
    description = models.CharField(max_length=250)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.description



class Products(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    price = models.IntegerField()
    is_available = models.CharField(max_length=2, choices=YES_NO_CHOICES, default="Si")
    photo = CloudinaryField('image')
    category = models.ForeignKey(ProductCategories, on_delete=models.CASCADE)
    id_company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Client(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone = models.CharField(max_length=100, blank=True)
    photo = models.CharField(max_length=4000)

    def __str__(self):
        return "{} {}".format(self.user.first_name, self.user.last_name)


class AddressSaved(models.Model):
    street = models.CharField(max_length=100)
    number = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    floor = models.CharField(max_length=100, blank=True, default='')
    reference = models.CharField(max_length=100, blank=True, default='')
    location = models.CharField(max_length=100, blank=True, default='')
    client = models.ForeignKey(Client, on_delete=models.CASCADE)


class State(models.Model):
    description = models.CharField(max_length=50)

    def __str__(self):
        return self.description


class Order(models.Model):
    id_company = models.ForeignKey(Company, on_delete=models.CASCADE)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    address = models.ForeignKey(AddressSaved, on_delete= models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)
    total = models.IntegerField()


class MeliLinks(models.Model):
    link = models.CharField(max_length=1024)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)


class DetailOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField()


# Business Rule: this must run every first day in every mount
class PaymentService(models.Model):
    company = models.ForeignKey(Company,on_delete=models.CASCADE)
    payment_date = models.DateField(auto_now_add=True)
    payment_status = models.CharField(max_length=45)
    mount = models.FloatField()
    transaction_date = models.DateField(null=True)
    description = models.CharField(max_length=45)
    period = models.CharField(max_length=45)


class MeLiTransaction(models.Model):
    preference_id = models.CharField(max_length=100)
    payment_id = models.CharField(max_length=45)
    payment_status = models.CharField(max_length=45)
    payment_status_detail = models.CharField(max_length=45)
    merchant_order_id = models.CharField(max_length=45)
    processing_mode = models.CharField(max_length=45)
    creation_date = models.DateTimeField(auto_now_add=True)
    payment_service = models.ForeignKey(PaymentService, on_delete=models.CASCADE)


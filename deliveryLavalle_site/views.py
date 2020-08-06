from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.template.defaultfilters import register

from core.models import Company, Client, Order, Products


def home(request):
    return render(request, 'deliveryLavalle_site/index.html')


@register.simple_tag()
def get_all_company():
    return Company.objects.all().count()


@register.simple_tag()
def get_all_users():
    return Client.objects.all().count()


@register.simple_tag()
def get_all_orders():
    return Order.objects.all().count()


@register.simple_tag()
def get_all_products():
    return Products.objects.all().count()

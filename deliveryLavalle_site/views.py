from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.template.defaultfilters import register

from core.models import Company, Client, Order, Products

def trigger_error(request):
    division_by_zero = 1 / 0

def home(request):
    context = {}
    if request.user.is_authenticated:
        company = Company.objects.filter(id_user=request.user.id).first()
        context = {'company': company}
    return render(request, 'deliveryLavalle_site/index.html', context)


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


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return render(request, 'deliveryLavalle_site/index.html')


def tutorial_meli_link(request):
    if request.user.is_authenticated:
        return render(request, 'deliveryLavalle_site/tutorial_meli_link.html')
    else:
        return render(request, 'deliveryLavalle_site/index.html')


def term_and_conditions(request):
    return render(request, 'deliveryLavalle_site/term_and_conditions.html')

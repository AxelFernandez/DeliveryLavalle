from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse

from core.models import Products


def change_stock_status(request, pk):
    new_status = request.POST.get('active')
    product = get_object_or_404(Products, id=pk)
    if new_status == 'activate':
        product.is_available = "SI"
    elif new_status == 'deactivate':
        product.is_available = "NO"
    product.save()
    return HttpResponseRedirect(reverse('product-list'))
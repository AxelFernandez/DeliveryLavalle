from django.contrib import admin

from core.models import Company, Order, Products, PaymentMethod, DetailOrder, Client, State, PaymentService, \
    AddressSaved

admin.site.register(Company)
admin.site.register(Order)
admin.site.register(Products)
admin.site.register(PaymentMethod)
admin.site.register(State)
admin.site.register(AddressSaved)
admin.site.register(DetailOrder)
admin.site.register(Client)
admin.site.register(PaymentService)

# Register your models here.

from django.contrib import admin

from core.models import Company, Order, Products, PaymentMethod, State, Chat, DetailOrder

admin.site.register(Company)
admin.site.register(Order)
admin.site.register(Products)
admin.site.register(PaymentMethod)
admin.site.register(State)
admin.site.register(Chat)
admin.site.register(DetailOrder)

# Register your models here.

from django.forms import ModelForm
from django import forms

from core.models import Company, Products


class FormCompany(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'description', 'phone', 'available_now', 'photo', 'limits']
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'id': 'name',
                    'class': 'form-control form-control-lg',
                    'placeholder': 'Mi super Empresa',
                }
            ),
            'description': forms.TextInput(
                attrs={
                    'id': 'description',
                    'class': 'form-control form-control-lg',
                    'placeholder': 'Venta de super Panchos y Empanadas',
                }
            ),
            'phone': forms.TextInput(
                attrs={
                    'id': 'phone',
                    'class': 'form-control form-control-lg',
                    'placeholder': '2613450277',
                }
            ),
            'available_now': forms.Select(
                attrs={
                    'id': 'available_now',
                    'class': 'form-control',
                }
            )
        }
        labels = {
            'name': 'Como se llama tu empresa?',
            'description': 'Que es lo que vendés?',
            'phone': 'Dejá tu numero de telefono para contactos',
            'available_now': 'Estás disponible para empezar a vender ahora?',
            'photo': 'Subí el logo de tu empresa',
            'limits': ''
        }


class FormProducts(forms.ModelForm):
    class Meta:
        model = Products
        fields = ['name', 'description', 'price', 'is_available', 'photo']
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'id': 'name',
                    'class': 'form-control form-control-lg',
                    'placeholder': 'Pizza',
                }
            ),
            'description': forms.TextInput(
                attrs={
                    'id': 'description',
                    'class': 'form-control form-control-lg',
                    'placeholder': 'Pizza muzzarela y aceitunas',
                }
            ),
            'is_available': forms.Select(
                attrs={
                    'id': 'available_now',
                    'class': 'form-control',
                }
            ),
            'price': forms.TextInput(
                attrs={
                    'id': 'price',
                    'class': 'form-control form-control-lg',
                    'placeholder': '$',
                }
            ),
        }
        labels = {
            'name': 'Nombre de tu Producto',
            'description': 'Una descripcion de tu producto',
            'is_available': 'Tenes Stock disponible?',
            'photo': 'Foto de tu Producto',
            'price': 'Precio de tu Producto',

        }

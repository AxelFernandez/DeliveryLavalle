from django.forms import ModelForm
from django import forms

from core.models import Company, Products


class FormCompany(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'description', 'address',  'phone', 'available_now', 'photo', 'limits']
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'id': 'name',
                    'class': 'form-control form-control-lg',
                    'placeholder': 'Nombre de la empresa ',
                }
            ),
            'description': forms.TextInput(
                attrs={
                    'id': 'description',
                    'class': 'form-control form-control-lg',
                    'placeholder': '¿Que es lo que vendés?',
                }
            ),
            'address': forms.TextInput(
                attrs={
                    'id': 'address',
                    'class': 'form-control form-control-lg',
                    'placeholder': 'Direccion',

                }
            ),
            'phone': forms.TextInput(
                attrs={
                    'id': 'phone',
                    'class': 'form-control form-control-lg',
                    'placeholder': 'Telefono',
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
            'name': '',
            'description': '',
            'address': '',
            'phone': '',
            'available_now': '¿Estás disponible para empezar a vender ahora?',
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
                    'placeholder': 'Nombre de tu Producto',
                }
            ),
            'description': forms.TextInput(
                attrs={
                    'id': 'description',
                    'class': 'form-control form-control-lg',
                        'placeholder': 'Descripcion de tu producto',
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
                    'class': 'form-control-lg',
                    'placeholder': 'Precio',
                }
            ),
        }
        labels = {
            'name': '',
            'description': '',
            'is_available': 'Tenes Stock disponible?',
            'photo': 'Foto de tu Producto',
            'price': '$',

        }

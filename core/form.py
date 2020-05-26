from django.forms import ModelForm
from django import forms

from core.models import Company


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
            )
        }
        labels = {
            'name': 'Como se llama tu empresa?',
            'description': 'Que es lo que vendés?',
            'phone': 'Dejá tu numero de telefono para contactos',
            'available_now': 'Estás disponible para empezar a vender ahora?',
            'photo': 'Subí el logo de tu empresa'
        }



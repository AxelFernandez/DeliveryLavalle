from django.forms import ModelForm
from django import forms

from core.models import Company, Products, PaymentMethod, MeliLinks, ProductCategories


class FormCompany(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'description','category', 'address',  'phone', 'payment_method', 'delivery_method', 'available_now', 'photo', 'limits']
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
            ),
            'category': forms.Select(
                attrs={
                    'id': 'category',
                    'class': 'form-control',
                }
            ),
            'payment_method': forms.CheckboxSelectMultiple(
                attrs={
                    'id': 'payment_method',
                    'label': 'hola'
                }
            ),
            'delivery_method': forms.CheckboxSelectMultiple(
                attrs={
                    'id': 'delivery_method',
                    'label': 'f'
                }
            )
        }
        labels = {
            'name': '',
            'description': '',
            'address': '',
            'category': 'Categoría',
            'phone': '',
            'payment_method': 'Selecciona los metodos de pago que Aceptas',
            'delivery_method': 'Selecciona los metodos de entrega',
            'available_now': '¿Estás disponible para empezar a vender ahora?',
            'photo': 'Subí el logo de tu empresa',
            'limits': ''
        }


class FormProducts(forms.ModelForm):
    class Meta:
        model = Products
        fields = ['name', 'description', 'price', 'category', 'is_available', 'photo']
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
            'category': forms.Select(
                attrs={
                    'id': 'category',
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
            'photo': forms.FileInput(
                attrs={
                    'id': 'photo',
                    'onchange': "previewFile()",
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


class FormMeliLinks(forms.ModelForm):
    class Meta:
        model = MeliLinks
        fields = ['link']
        widgets = {
            'link': forms.TextInput(
                attrs={
                    'id': 'link',
                    'class': 'form-control form-control-lg',
                    'placeholder': 'Link de Pago',
                }
            ),

        }
        labels = {
            'link': '',
        }


class FormCategory(forms.ModelForm):
    class Meta:
        model = ProductCategories
        fields = ['description']
        widgets = {
            'description': forms.TextInput(
                attrs={
                    'id': 'description',
                    'class': 'form-control form-control-lg',
                    'placeholder': 'Descripción de la Categoria',
                }
            )
        }
        labels = {
            'description': '',
        }

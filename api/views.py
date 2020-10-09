import ast

from django.shortcuts import render

# Create your views here.
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.utils.datetime_safe import datetime
from rest_framework.permissions import IsAuthenticated
from rest_framework.utils import json
from rest_framework.views import APIView
from rest_framework.response import Response
import requests
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User

from core.models import Client, Company, Products, Order, State, AddressSaved, PaymentMethod, DetailOrder, \
    CompanyCategory, ProductCategories


class ClientApi(APIView):
    permission_classes = (IsAuthenticated,)

    # Use /api/client?client_id=1
    def get(self, request):
        client_id = request.query_params.get('id')
        if client_id is None:
            return Response({'message': 'Must specify an Client id'})
        client = Client.objects.get(pk=client_id)
        content = {'clientid': client.pk,
                   'email': client.user.email,
                   'givenName': client.user.first_name,
                   'familyName': client.user.last_name,
                   'photo': client.photo,
                   'phone': client.phone,
                   'username': client.user.username,
                   }
        return Response(content)

    def post(self, request):
        id = request.data.get("clientId")

        phone = request.data.get("phone")
        if id is None or phone is None:
            return Response({'message': 'Not enought arguments Id {}, first Name is {}, last name is {}, phone is {}'.format(id, phone)}, status=400)
        client = Client.objects.get(pk=id)
        client.phone = phone
        client.save()
        content = {'clientid': client.pk,
                   'email': client.user.email,
                   'givenName': client.user.first_name,
                   'familyName': client.user.last_name,
                   'photo': client.photo,
                   'phone': client.phone,
                   'username': client.user.username,
                   }
        return Response(content)


class GoogleView(APIView):

    # Send a Body {"token": TOKEN_HERE}
    def post(self, request):

        # create user if not exist
        is_new = False
        soft_account = False
        try:
            user = User.objects.get(email=request.data.get('email'))
        except User.DoesNotExist:
            user = User()
            user.username = request.data.get('email')
            # provider random default password
            user.password = make_password(BaseUserManager().make_random_password())
            user.email = request.data.get('email')
            user.first_name = request.data.get('givenName')
            user.last_name = request.data.get('familyName')
            is_new = True
            user.save()
        try:
            client = Client.objects.get(user=user)
        except Client.DoesNotExist:
            client = Client()
            client.user = user
            client.photo = request.data.get('photo')
            client.phone = request.data.get('phone')

            if client.photo is None or client.phone is None:
                soft_account = True
            client.save()
        token = RefreshToken.for_user(user)  # generate token without username & password
        response = {"is_new": is_new,
                    "completeRegistry": soft_account,
                    "clientId": client.pk,
                    "username": user.username,
                    "access_token": str(token.access_token),
                    "refresh_token": str(token)
                    }
        return Response(response)


class MethodApi(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        company_id = request.data
        company = Company.objects.get(pk=company_id)
        methods = []
        for method in company.payment_method.all():
            methods.append(method.description)
        company_response = {
            'methods': methods,
        }
        return Response(company_response)


class CompanyApi(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        category = request.data.get('category')
        lat = float(request.data.get('lat'))
        long = float(request.data.get('long'))
        if lat is None or long is None:
            return Response({'message': 'Latitude or Longitude not Found'}, status=400)
        company_list = self.find_company_near(lat, long, category)
        company_array = []

        for company in company_list:
            methods = []
            if company.available_now == "SI":
                for method in company.payment_method.all():
                    methods.append(method.description)
                for delivery_method in company.delivery_method.all():
                    methods.append(delivery_method.description)
                company_response = {
                    'methods': methods,
                    'id': company.pk,
                    'name': company.name,
                    'description': company.description,
                    'photo': company.photo.url,
                    'category': company.category.description,
                }
                company_array.append(company_response)
        return Response(company_array)

    def find_company_near(self, lat, long, description=None):
        if description is None:
            company_all = Company.objects.all().order_by('category')
        else:
            category = CompanyCategory.objects.get(description=description)
            company_all = Company.objects.filter(category=category)
        company_list = []
        for company in company_all:
            limits = ast.literal_eval(company.limits)
            if limits.get('north') > lat > limits.get('south') \
                    and limits.get('east') > long > limits.get('west'):
                company_list.append(company)
        return company_list


class CompanyDetailApi(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        comapny_id = request.data
        company = Company.objects.get(pk=comapny_id)
        methods = []
        for method in company.payment_method.all():
            methods.append(method.description)
        for delivery_method in company.delivery_method.all():
            methods.append(delivery_method.description)
        company_response = {
            'methods': methods,
            'id': company.pk,
            'name': company.name,
            'description': company.description,
            'address': company.address,
            'photo': company.photo.url,
            'category': company.category.description,
        }
        return Response(company_response)


class ProductApi(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        comapny_id = request.data.get('companyId')
        categoty = request.data.get('category')
        if categoty is None:
            products = Products.objects.filter(id_company=comapny_id)
        else:
            category_object = ProductCategories.objects.get(description= categoty)
            products = Products.objects.filter(id_company=comapny_id,category= category_object)
        products_array = []
        for product in products:
            if product.is_available:
                item = {
                    'id': product.pk,
                    'name': product.name,
                    'description': product.description,
                    'price': product.price,
                    'photo': product.photo.url,
                    'category': product.category.description,
                }
                products_array.append(item)
        return Response(products_array)

class AddressDelete(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        id = request.data.get("id")
        AddressSaved.objects.get(pk=id).delete()
        return Response(id)


class AddressApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        client = Client.objects.get(user=self.request.user)
        addresses = AddressSaved.objects.filter(client=client)
        address_array = []
        for address in addresses:
            item = {
                'id': address.pk,
                'street': address.street,
                'number': address.number,
                'district': address.district,
                'floor': address.floor,
                'reference': address.reference,
                'location': address.location,
            }
            address_array.append(item)
        return Response(address_array)

    def post(self, request):
        street = request.data.get("street")
        number = request.data.get("number")
        district = request.data.get("district")
        floor = request.data.get("floor")
        reference = request.data.get("reference")
        location = request.data.get("location")
        address = AddressSaved()
        address.street = street
        address.number = number
        address.district = district
        address.floor = floor
        address.reference = reference
        address.location = location
        address.client = Client.objects.get(user=self.request.user)
        address.save()
        return Response({
            'addressId': address.pk
        })

class CompanyCategories(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        categories = CompanyCategory.objects.all()
        category_array = []
        for category in categories:
            item = {
                'description': category.description,
                'photo': category.photo,
            }
            category_array.append(item)

        return Response(category_array)

class ProductCategoriesByCompany(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        company_id = request.data
        company = Company.objects.get(pk=company_id)
        categories = ProductCategories.objects.filter(company = company)
        category_array = []
        for category in categories:
            item = {
                'description': category.description,
            }
            category_array.append(item)

        return Response(category_array)

class OrderApi(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        company = request.data.get("company")
        address = request.data.get("address_id")
        payment_method = request.data.get("payment_method")
        total = request.data.get("total")
        items = request.data.get("items")
        if  payment_method is None \
                or total is None or items is None:
            return Response({'message': 'Some Atribute is not Found'}, status=400)
        client = Client.objects.get(user=self.request.user)

        order = Order()
        order.id_company = Company.objects.get(pk=company)
        order.state = State.objects.get(pk=1)
        order.address = AddressSaved.objects.get(pk=address)
        order.client = client
        order.payment_method = PaymentMethod.objects.get(description=payment_method)
        order.total = int(total)
        order.save()

        for item in items:
            detail_order = DetailOrder()
            detail_order.order = order
            detail_order.product = Products.objects.get(pk=item.get('product_id'))
            detail_order.quantity = item.get('quantity')
            detail_order.save()

        response = {'date_created': order.date,
                    'order_id': order.pk,
                    'state': order.state.description,
                    }
        return Response(response)

    def get(self, request):
        client = Client.objects.get(user=self.request.user)
        orders = Order.objects.filter(client=client)
        orders_array = []
        for order in orders:
            address = "{} {}, {}".format(order.address.street,
                                         order.address.number,
                                         order.address.district)
            item = {
                'company': order.id_company.name,
                'state': order.state.description,
                'address': address,
                'payment_method': order.payment_method.description,
                'total': order.total,
            }
            orders_array.append(item)

        return Response(orders_array)

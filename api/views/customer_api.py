import ast

from django.db.models import Avg
from django.shortcuts import render

# Create your views here.
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.utils import formats, timezone
from django.utils.datetime_safe import datetime
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.utils import json
from rest_framework.views import APIView
from rest_framework.response import Response
import requests
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User

from core.models import Client, Company, Products, Order, State, AddressSaved, PaymentMethod, DetailOrder, \
    CompanyCategory, ProductCategories, MeliLinks, FirebaseToken, Reviews
from core.views.OrdersViews import send_notification_to_seller


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
            user.email = request.data.get('email').split("@")[0]
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

class MethodDeliveryApi(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        company_id = request.data
        company = Company.objects.get(pk=company_id)
        methods = []
        for method in company.delivery_method.all():
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
            if company.available_now:
                for method in company.payment_method.all():
                    methods.append(method.description)
                for delivery_method in company.delivery_method.all():
                    methods.append(delivery_method.description)
                company_response = {
                    'methods': methods,
                    'rating': company.average_rating,
                    'id': company.pk,
                    'name': company.name,
                    'phone': company.phone,
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
            'rating': company.average_rating,
            'address': company.address,
            'phone': company.phone,
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
            products = Products.objects.filter(id_company=comapny_id, is_active=True)
        else:
            category_object = ProductCategories.objects.get(description=categoty)
            products = Products.objects.filter(id_company=comapny_id, category=category_object, is_active=True)
        products_array = []
        for product in products:
            # TODO: Please, Refactor me ASAP!
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
        address = AddressSaved.objects.get(pk=id)
        address.is_active = False
        address.save()
        return Response(id)


class AddressApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        client = Client.objects.get(user=self.request.user)
        addresses = AddressSaved.objects.filter(client=client)
        address_array = []
        for address in addresses:
            if address.is_active:
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
        address.isActive = True
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
        company = request.data.get("companyId")
        address = request.data.get("addressId")
        payment_method = request.data.get("paymentMethod")
        retry_in_local_request = request.data.get("retryInLocal")
        total = request.data.get("total")
        items = request.data.get("items")
        if  payment_method is None \
                or total is None or items is None:
            return Response({'message': 'Some Atribute is not Found'}, status=400)
        client = Client.objects.get(user=self.request.user)
        company = Company.objects.get(pk=company)

        if not company.available_now:
            return Response({'state': "Cancelado",
                             'responseCode': 400})

        order = Order()
        order.id_company = company
        order.state = State.objects.get(pk=1)
        order.retry_in_local = retry_in_local_request
        if not retry_in_local_request:
            order.address = AddressSaved.objects.get(pk=address)
        order.client = client
        order.payment_method = PaymentMethod.objects.get(description=payment_method)
        order.total = int(total)
        order.save()

        for item in items:
            detail_order = DetailOrder()
            detail_order.order = order
            detail_order.product = Products.objects.get(pk=item.get('id'))
            detail_order.quantity = item.get('quantity')
            detail_order.save()

        response = {'dateCreated': formats.date_format(timezone.localtime(order.date), "d/m/Y H:i"),
                    'orderId': order.pk,
                    'state': order.state.description,
                    'responseCode': 200
                    }
        title = "Hay un nuevo pedido Pendiente"
        text = "{} esta esperando a que lo confirmes".format(client.user.first_name)
        send_notification_to_seller(order, text, title)
        return Response(response)

    def get(self, request):
        client = Client.objects.get(user=self.request.user)
        orders = Order.objects.filter(client=client).order_by('-pk')
        if request.data.get("orderId") is not None:
            id_order = request.data.get("orderId")
            orders = Order.objects.get(pk=id_order)
        orders_array = []
        for order in orders:
            details = DetailOrder.objects.filter(order=order)
            detail_array = []
            for detail in details:
                product = Products.objects.get(pk=detail.product.id)
                subtotal = product.price * detail.quantity
                item_detail = {
                    'id': product.id,
                    'quantity': detail.quantity,
                    'description': product.description,
                    'subtotal': subtotal,
                }
                detail_array.append(item_detail)
            company_order = order.id_company
            methods = []
            for method in company_order.payment_method.all():
                methods.append(method.description)
            for delivery_method in company_order.delivery_method.all():
                methods.append(delivery_method.description)
            address = {}
            if not order.retry_in_local:
                address_order = order.address
                address = {
                    'id': address_order.pk,
                    'street': address_order.street,
                    'number': address_order.number,
                    'district': address_order.number,
                    'floor': address_order.floor,
                    'reference': address_order.reference,
                }
            company = {
                'id': company_order.pk,
                'name': company_order.name,
                'description': company_order.description,
                'photo': company_order.photo.url,
                'phone': company_order.phone,
                'address': company_order.address,
                'methods': methods,
                'category': company_order.category.description,
            }
            order.date = formats.date_format(timezone.localtime(order.date), "d/m/Y H:i")
            item = {
                'id': order.pk,
                'company': company,
                'state': order.state.description,
                'address': address,
                'dateCreated': order.date,
                'retryInLocal': order.retry_in_local,
                'paymentMethod': order.payment_method.description,
                'total': order.total,
                'items': detail_array
            }
            orders_array.append(item)

        return Response(orders_array)


class OrderById(APIView):
    permission_classes = (IsAuthenticated,)


    def post(self, request):
        id_order = request.data
        order = Order.objects.get(pk=id_order)
        details = DetailOrder.objects.filter(order=order)
        detail_array = []
        for detail in details:
            product = Products.objects.get(pk=detail.product.id)
            subtotal = product.price * detail.quantity
            item_detail = {
                'id': product.id,
                'quantity': detail.quantity,
                'description': product.description,
                'subtotal': subtotal,
            }
            detail_array.append(item_detail)
        company_order = order.id_company
        methods = []
        for method in company_order.payment_method.all():
            methods.append(method.description)
        for delivery_method in company_order.delivery_method.all():
            methods.append(delivery_method.description)
        address = {}
        if not order.retry_in_local:
            address_order = order.address
            address = {
                'id': address_order.pk,
                'street': address_order.street,
                'number': address_order.number,
                'district': address_order.number,
                'floor': address_order.floor,
                'reference': address_order.reference,
            }
        company = {
            'id': company_order.pk,
            'name': company_order.name,
            'description': company_order.description,
            'photo': company_order.photo.url,
            'phone': company_order.phone,
            'address': company_order.address,
            'methods': methods,
            'category': company_order.category.description,
        }
        item = {
            'id': order.pk,
            'company': company,
            'state': order.state.description,
            'address': address,
            'dateCreated': order.date,
            'retryInLocal': order.retry_in_local,
            'paymentMethod': order.payment_method.description,
            'total': order.total,
            'items': detail_array
        }
        return Response(item)



class MeliLinkApi(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self,request):
        order_id = request.data
        try:
           meli_link = MeliLinks.objects.get(order= order_id)
        except:
            return Response(
                {
                    "isAvailable": False
                }
            )
        return Response(
            {
                "isAvailable": True,
                "link": meli_link.link
            }
        )


class Review(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        company = request.query_params.get('company')
        reviews = Reviews.objects.filter(company=company)
        response = []
        for review in reviews:
            item = {
                'userName': "{} {}".format(review.user.first_name, review.user.last_name),
                'rating': review.rating,
                'description': review.description,
            }
            response.append(item)
        return Response(response)


class Rating(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        order_id = request.query_params.get('order')
        try:
            order = Order.objects.get(pk=order_id)
            review = Reviews.objects.get(order=order)
            return Response({
                'description': review.description,
                'rating': review.rating
            })
        except Reviews.DoesNotExist:
            return Response({
                'rating': -1
            })

    def post(self, request, *args, **kwargs):
        order_id = request.data.get("order")
        rating = request.data.get("rating")
        description = request.data.get("description")
        order = Order.objects.get(pk=order_id)
        try:
            review = Reviews()
            review.order = order
            review.description = description
            review.rating = rating
            review.company = order.id_company
            review.user = request.user
            review.save()
            get_average_from_company(order.id_company)
            return Response(review.pk)
        except:
            raise ValidationError()


class FirebaseTokenApi(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        token = request.data.get("token")
        is_seller = request.data.get("isSeller")
        user = User.objects.get(email=request.user.email)
        tokens = FirebaseToken.objects.filter(token=token)
        if len(tokens) == 0:
            firebase_token = FirebaseToken()
            firebase_token.user = user
            firebase_token.token = token
            firebase_token.is_seller = is_seller
            firebase_token.save()
        return Response({"done": True})


def get_average_from_company(company):
    avg = Reviews.objects.filter(company=company).aggregate(Avg('rating'))
    rating = avg.get("rating__avg")
    company.average_rating = round(rating, 1)
    company.save()

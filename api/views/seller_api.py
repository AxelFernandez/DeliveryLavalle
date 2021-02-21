import ast
import urllib
import requests
import json

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.utils import formats, timezone
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken


from api.views.customer_api import format_client
from core import models
from core.models import Company, CompanyCategory, PaymentMethod, DeliveryMethod, Order, State, DetailOrder, Products, \
    ProductCategories, MeliLinks, PaymentService, GoogleIdUsers
from core.views.Companyviews import get_company
from core.views.OrdersViews import get_next_state, cancel_order, send_notification_to_customers


class GoogleViewSeller(APIView):
    # TODO: Refactor this for a common Login
    # Send a Body {"token": TOKEN_HERE}
    def post(self, request):

        # create user if not exist
        is_new = False
        soft_account = True
        url = "https://oauth2.googleapis.com/tokeninfo?id_token={}".format(request.data)
        request = requests.get(url)
        response = json.loads(request.text)
        google_internal_id = response.get('sub')
        if google_internal_id is None:
            Response('Invalid Token', 400)
        try:
            user = GoogleIdUsers.objects.get(sub_google_id=google_internal_id).user
        except GoogleIdUsers.DoesNotExist:

            user = User()
            user.username = response.get('name')
            # provider random default password
            user.password = make_password(BaseUserManager().make_random_password())
            user.email = response.get('email')
            user.first_name = response.get('given_name')
            if response.get('family_name') is None:
                user.last_name = ""
            else:
                user.last_name = response.get('family_name')
            is_new = True
            user.save()

            google_sub = GoogleIdUsers()
            google_sub.sub_google_id = google_internal_id
            google_sub.user = user
            google_sub.save()
        try:
            company = Company.objects.get(id_user=user)
        except Company.DoesNotExist:
            soft_account = False

        token = RefreshToken.for_user(user)  # generate token without username & password

        user_formated = {
                'email': user.email,
                'givenName': user.first_name,
                'familyName': user.last_name,
                'photo': response.get("picture"),
                'username': user.username,
                }
        response = {"is_new": is_new,
                    "completeRegistry": soft_account,
                    "username": user.username,
                    "userId": user.pk,
                    "access_token": str(token.access_token),
                    "refresh_token": str(token),
                    "user": user_formated
                    }
        return Response(response)


class CreateCompany(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        comapny_from_user = request.user
        company = Company.objects.get(id_user=comapny_from_user)
        payment_method = []
        delivery_method = []
        for method in company.payment_method.all():
            payment_method.append(method.description)
        for method in company.delivery_method.all():
            delivery_method.append(method.description)

        company_response = {
            'paymentMethods': payment_method,
            'deliveryMethods': delivery_method,
            'id': company.pk,
            'name': company.name,
            'availableNow': company.available_now,
            'description': company.description,
            'address': company.address,
            'rating': company.average_rating,
            'phone': company.phone,
            'photo': company.photo.url,
            'category': company.category.description,
            'limits': company.limits

        }
        return Response(company_response)

    def post(self, request):
        name = request.data.get("name")
        description = request.data.get("description")
        phone = request.data.get("phone")
        address = request.data.get("address")
        available_now = request.data.get("availableNow")
        photo = request.data.get("image")
        limits = request.data.get("limits")
        category_description = request.data.get("category")
        limits = urllib.parse.unquote(limits.__str__())
        category_selected = CompanyCategory.objects.get(description=category_description)
        payment_array = []
        delivery_array = []

        if available_now.__str__() == "true" or available_now:
            available_now = True
        else:
            available_now = False
        try:
            payment_methods = request.data.get("paymentMethods").name
            payment_methods = payment_methods.replace('[', '')
            payment_methods = payment_methods.replace(']', '')
            payment_methods = payment_methods.split(',')
        except:
            payment_methods = request.data.get("paymentMethods")

        try:
            delivery_methods = request.data.get("deliveryMethods").name
            delivery_methods = delivery_methods.replace('[', '')
            delivery_methods = delivery_methods.replace(']', '')
            delivery_methods = delivery_methods.split(',')
        except:
            delivery_methods = request.data.get("deliveryMethods")

        try:
            comapny_from_user = request.user
            company = Company.objects.get(id_user=comapny_from_user)
        except:
            company = Company()
            company.account_debit = 0

        try:
            company.name = name
            company.description = description
            company.phone = phone
            company.address = address
            company.available_now = available_now
            if photo is not None:
                company.photo = photo
            company.limits = limits
            company.category = category_selected
            company.id_user = request.user
            company.save()
            for method in payment_methods:
                method = method.strip()
                method_selected = PaymentMethod.objects.get(description=method)
                payment_array.append(method_selected)
            company.payment_method.set(payment_array)

            for method in delivery_methods:
                method = method.strip()
                delivery_method_selected = DeliveryMethod.objects.get(description=method)
                delivery_array.append(delivery_method_selected)
            company.delivery_method.set(delivery_array)

            company.save()
        except Exception():
            return Response({"Error Saving This"}, 400)

        return Response(company.pk)


class MeliLinkSeller(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        order_id = request.data.get("orderId")
        link = request.data.get("link")
        try:
            order = Order.objects.get(pk=order_id)
            meli_link = MeliLinks.objects.get(order=order)
        except:
            meli_link = MeliLinks()
        try:
            meli_link.order = order
            meli_link.link = link
            meli_link.save()
            title = "Esta disponible tu Link de Pago de " + order.id_company.name
            body = "Entra a la app y buscalo en mis ordenes"
            send_notification_to_customers(order, body, title)
        except:
            raise Exception(
                "An error was found in the Meli Link Seller when is saved orderid: {} , Link: {}".format(order_id,
                                                                                                         link))
        return Response(meli_link.pk)


class GetOrdersPending(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        company = Company.objects.get(id_user=request.user)
        state = State.objects.get(description='Pendiente')
        orders = Order.objects.filter(id_company=company, state=state)

        response = []
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

            order.date = formats.date_format(timezone.localtime(order.date), "d/m/Y H:i")
            client = {
                'name': "{} {}".format(order.client.user.first_name, order.client.user.last_name),
                'email': order.client.user.email,
                'photo': order.client.photo,
                'phone': order.client.phone
            }
            item = {

                'id': order.pk,
                'state': order.state.description,
                'address': address,
                'dateCreated': order.date,
                'retryInLocal': order.retry_in_local,
                'paymentMethod': order.payment_method.description,
                'total': order.total,
                'client': client,
                'items': detail_array
            }
            response.append(item)

        return Response(response)


class GetOrdersPending(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        company = Company.objects.get(id_user=request.user)
        state = State.objects.get(description='Pendiente')
        orders = Order.objects.filter(id_company=company, state=state).order_by('-pk')
        return Response(format_orders(orders))


class GetOrdersInProgress(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        company = Company.objects.get(id_user=request.user)
        state = State.objects.filter(
            Q(description='En preparación') | Q(description='En Camino') | Q(description='Listo para Retirar'))
        orders = Order.objects.filter(id_company=company, state__in=state).order_by('-pk')
        return Response(format_orders(orders))


class ProductsCategory(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        company = Company.objects.get(id_user=request.user)
        category = ProductCategories.objects.filter(company=company, is_active=True)
        return Response(format_category(category))

    def post(self, request):
        description = request.data.get('description')
        id = request.data.get('id')
        company = Company.objects.get(id_user=request.user)
        if id is not None:
            category = ProductCategories.objects.get(pk=id)
        else:
            category = ProductCategories()
        category.company = company
        category.description = description
        category.save()

        return Response(format_category([category]))


class ProductCategoryDelete(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        id = request.data.get('id')
        category = ProductCategories.objects.get(pk=id)
        count_product = Products.objects.filter(category=category, is_active=True).count()
        if count_product != 0:
            return Response('', 400)
        else:
            category.is_active = False
            category.save()
            return Response('', 200)


class ProductDelete(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        id = request.data.get('id')
        product = Products.objects.get(pk=id)
        product.is_active = False
        product.save()
        return Response(id)


class GetOrdersClosed(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        company = Company.objects.get(id_user=request.user)
        state = State.objects.filter(Q(description='Cancelado') | Q(description='Entregado'))
        orders = Order.objects.filter(id_company=company, state__in=state).order_by('-pk')
        return Response(format_orders(orders))


class Product(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        company = Company.objects.get(id_user=request.user)
        products = Products.objects.filter(id_company=company, is_active=True)
        products_array = []
        for product in products:
            if product.is_active or product.is_available:
                item = {
                    'id': product.pk,
                    'name': product.name,
                    'description': product.description,
                    'price': product.price,
                    'photo': product.photo.url,
                    'category': product.category.pk,
                    'availableNow': product.is_available
                }
                products_array.append(item)
        return Response(products_array)

    def post(self, request):
        name = request.data.get("name").__str__()
        description = request.data.get("description").__str__()
        category_description = request.data.get("category").__str__()
        price = request.data.get("price").__str__()
        available_now = request.data.get("availableNow")
        photo = request.data.get("image")
        id = request.data.get("id")
        company = Company.objects.get(id_user=request.user)
        category_selected = ProductCategories.objects.get(pk=category_description)
        if available_now.__str__() == "true" or available_now is True:
            available_now = True
        else:
            available_now = False
        if id is None:
            product = Products()
        else:
            product = Products.objects.get(pk=id.__str__())
        try:
            product.name = urllib.parse.unquote_plus(name)
            product.description = urllib.parse.unquote_plus(description)
            product.category = category_selected
            if photo is not None:
                product.photo = photo
            product.price = int(price)
            product.is_available = available_now
            product.id_company = company
            product.is_active = True
            product.save()
        except Exception as e:
            raise e
        return Response(product.pk)


class GetOrdersById(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        orderId = request.data
        orders = Order.objects.get(pk=orderId)
        return Response(format_order_separate(orders))


class SetOrdersInNewState(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        orderId = request.data
        get_next_state(request, orderId)
        orders = Order.objects.get(pk=orderId)
        return Response(format_order_separate(orders))


class CancelOrder(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        orderId = request.data
        cancel_order(request, orderId)
        orders = Order.objects.get(pk=orderId)
        return Response(format_order_separate(orders))


class AccountDebit(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        company = Company.objects.get(id_user=request.user)
        return Response(company.account_debit)


def format_category(categories):
    arrayCategory = []
    for category in categories:
        item = format_category_separate(category)
        arrayCategory.append(item)
    return arrayCategory


def format_category_separate(category):
    products = Products.objects.filter(category=category, is_active=True).count()
    item = {
        'id': category.pk,
        'description': category.description,
        'quantity': products
    }
    return item

def format_order_separate(order):
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
            'location': address_order.location,
        }

    order.date = formats.date_format(timezone.localtime(order.date), "d/m/Y H:i")
    client = {
        'name': "{} {}".format(order.client.user.first_name, order.client.user.last_name),
        'email': order.client.user.email,
        'photo': order.client.photo,
        'phone': order.client.phone
    }
    item = {

        'id': order.pk,
        'state': order.state.description,
        'address': address,
        'dateCreated': order.date,
        'retryInLocal': order.retry_in_local,
        'paymentMethod': order.payment_method.description,
        'total': order.total,
        'client': client,
        'items': detail_array
    }
    return item


def format_orders(orders):
    response = []
    for order in orders:
        response.append(format_order_separate(order))
    return response


class InvoiceApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        company = get_company(request.user)
        invoices = PaymentService.objects.filter(company=company)
        array_result = []
        for invoice in invoices:
            response = {
                'period': invoice.period,
                'mount': invoice.mount,
                'status': invoice.payment_status,
                'dateCreated': invoice.payment_date,
                'datePayed': invoice.transaction_date,
            }
            array_result.append(response)
        return Response(array_result)


class CompanyAvailability(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        company = get_company(request.user)
        return Response(company.available_now)

    def post(self, request):
        availability = request.data
        company = get_company(request.user)
        company.available_now = availability
        company.save()
        return Response(company.available_now)


class InvoicePendingApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        company = get_company(request.user)
        invoices = PaymentService.objects.filter(company=company, payment_status='Pendiente')
        if len(invoices) == 0:
            return Response(False)
        else:
            return Response(True)

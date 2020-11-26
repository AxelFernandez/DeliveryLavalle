import ast
import urllib

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

from core.models import Company, CompanyCategory, PaymentMethod, DeliveryMethod


class GoogleViewSeller(APIView):

    # Send a Body {"token": TOKEN_HERE}
    def post(self, request):

        # create user if not exist
        is_new = False
        soft_account = True
        try:
            user = User.objects.get(email=request.data.get('email'))
        except User.DoesNotExist:
            user = User()
            user.username = request.data.get('email').split("@")[0]
            # provider random default password
            user.password = make_password(BaseUserManager().make_random_password())
            user.email = request.data.get('email')
            user.first_name = request.data.get('givenName')
            user.last_name = request.data.get('familyName')
            is_new = True
            user.save()
        try:
            company = Company.objects.get(id_user=user)
        except Company.DoesNotExist:
            soft_account = False

        token = RefreshToken.for_user(user)  # generate token without username & password
        response = {"is_new": is_new,
                    "completeRegistry": soft_account,
                    "username": user.username,
                    "userId": user.pk,
                    "access_token": str(token.access_token),
                    "refresh_token": str(token)
                    }
        return Response(response)


class CreateCompany(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        name = request.data.get("name")
        description = request.data.get("description")
        phone = request.data.get("phone")
        address = request.data.get("address")
        available_now = request.data.get("availableNow")
        photo = request.data.get("image")
        limits = request.data.get("limits")
        category_description = request.data.get("category")
        payment_methods = request.data.get("paymentMethod").name
        delivery_methods = request.data.get("deliveryMethod").name
        limits = urllib.parse.unquote(limits.__str__())
        category_selected = CompanyCategory.objects.get(description=category_description)

        payment_array = []
        payment_methods = payment_methods.replace('[', '')
        payment_methods = payment_methods.replace(']', '')
        payment_methods = payment_methods.split(',')

        delivery_array = []
        delivery_methods = delivery_methods.replace('[', '')
        delivery_methods = delivery_methods.replace(']', '')
        delivery_methods = delivery_methods.split(',')
        company = Company()
        try:
            company.name = name
            company.description = description
            company.phone = phone
            company.address = address
            company.available_now = available_now
            company.photo = photo
            company.limits = limits
            company.category = category_selected
            company.account_debit = 0
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



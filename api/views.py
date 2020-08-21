from django.shortcuts import render

# Create your views here.
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import IsAuthenticated
from rest_framework.utils import json
from rest_framework.views import APIView
from rest_framework.response import Response
import requests
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User

from core.models import Client


class ClientApi(APIView):
    permission_classes = (IsAuthenticated,)

    # Use /api/client?client_id=1
    def get(self, request):
        client_id = request.query_params.get('id')
        if client_id is None:
            return Response({'message': 'Must specify an Client id'})
        client = Client.objects.get(pk=client_id)
        content = {'id': client.pk,
                   'phone': client.phone,
                   'photo': client.photo,
                   'email': client.user.email,
                   'name': "{} {}".format(client.user.first_name, client.user.last_name)
                   }
        return Response(content)

    def post(self, request):
        id = request.data.get("id")
        first_name = request.data.get("first_name")
        last_name = request.data.get("last_name")
        phone = request.data.get("phone")
        if id is None or first_name is None or last_name is None or phone is None:
            return Response({'message': 'Not enought arguments  '
                                        'Id {}, first Name is {}, last name is {}, phone is {}'.format(id, first_name, last_name, phone)}, status=400)
        client = Client.objects.get(pk=id)
        client.phone = phone
        client.save()

        user = User.objects.get(pk=client.user.pk)
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        content = {
            "id": client.pk,
            "first_name": client.user.first_name,
            "last_name": client.user.last_name,
            "phone": client.phone,

        }
        return Response(content)


class GoogleView(APIView):

    # Send a Body {"token": TOKEN_HERE}
    def post(self, request):
        payload = {'access_token': request.data.get("token"), 'alt': 'json'}  # validate the token
        r = requests.get('https://www.googleapis.com/oauth2/v2/userinfo', params=payload)
        data = json.loads(r.text)

        if 'error' in data:
            content = {'message': 'wrong google token / this google token is already expired.'}
            return Response(content,status=400)

        # create user if not exist
        is_new = False
        try:
            user = User.objects.get(email=data['email'])
            client = Client.objects.get(user=user)
        except User.DoesNotExist:
            user = User()
            user.username = data['email']
            # provider random default password
            user.password = make_password(BaseUserManager().make_random_password())
            user.email = data['email']
            is_new = True
            user.save()

            client = Client()
            client.user = user
            client.photo = data['picture']
            client.save()

        token = RefreshToken.for_user(user)  # generate token without username & password
        response = {"is_new": is_new,
                    "client_id": client.pk,
                    "username": user.username,
                    "access_token": str(token.access_token),
                    "refresh_token": str(token)
                    }
        return Response(response)


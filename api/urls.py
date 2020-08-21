from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from api.views import GoogleView, ClientApi

urlpatterns = [
    path('google', GoogleView.as_view(), name='google'),

    path('client', ClientApi.as_view(), name='client'),

]
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from api.views.customer_api import FirebaseTokenApi, CompanyCategories
from api.views.seller_api import GoogleViewSeller, CreateCompany

urlpatterns = [
    path('google', GoogleViewSeller.as_view(), name='google'),
    path('firebase_token', FirebaseTokenApi.as_view(), name='firebase-token'),

    path('company_category', CompanyCategories.as_view(), name='comapny-category-api'),
    path('company', CreateCompany.as_view(), name='google')

]
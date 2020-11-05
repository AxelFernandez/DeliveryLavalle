from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from api.views import GoogleView, ClientApi, CompanyApi, CompanyDetailApi, ProductApi, AddressApi, OrderApi, \
    CompanyCategories, ProductCategoriesByCompany, AddressDelete, MethodApi, MethodDeliveryApi, OrderById, MeliLinkApi, \
    FirebaseTokenApi

urlpatterns = [
    path('google', GoogleView.as_view(), name='google'),

    path('client', ClientApi.as_view(), name='client-api'),
    path('company', CompanyApi.as_view(), name='company-api'),
    path('company_detail', CompanyDetailApi.as_view(), name='company-details-api'),
    path('product', ProductApi.as_view(), name='product-api'),
    path('address', AddressApi.as_view(), name='address-api'),
    path('address_delete', AddressDelete.as_view(), name='address-delete'),
    path('payment_method', MethodApi.as_view(), name='payment_method'),
    path('delivery_method', MethodDeliveryApi.as_view(), name='payment_delivery_method'),
    path('order', OrderApi.as_view(), name='order-api'),
    path('order_by_id', OrderById.as_view(), name='order-by-id-api'),
    path('meli_link', MeliLinkApi.as_view(), name='meli-link-api'),
    path('firebase_token', FirebaseTokenApi.as_view(), name='firebase-token'),
    path('company_category', CompanyCategories.as_view(), name='comapny-category-api'),
    path('product_category', ProductCategoriesByCompany.as_view(), name='comapny-category-api'),

]
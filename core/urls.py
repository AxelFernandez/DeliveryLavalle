from django.urls import include, path
from .views import register, RegistryCompany, CompanyRegistered, CreateProducts

urlpatterns = [
    path('', include('django.contrib.auth.urls'), name="login"),
    path('register/', register, name='register'),
    path('oauth/', include('social_django.urls', namespace='social')),
    path('company/', RegistryCompany.as_view(), name='company'),
    path('company_registered/<pk>', CompanyRegistered.as_view(), name='company_registered'),
    path('products/create', CreateProducts.as_view(), name='create-products')
]

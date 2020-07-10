from django.urls import include, path
from .views import register, RegistryCompany, CompanyRegistered, CreateProducts, ProductsList, ProductEdit, ProductDelete, change_stock_status

urlpatterns = [
    path('', include('django.contrib.auth.urls'), name="login"),
    path('home/', register, name='home'),
    path('oauth/', include('social_django.urls', namespace='social')),
    path('company/', RegistryCompany.as_view(), name='company'),
    path('company_registered/<pk>', CompanyRegistered.as_view(), name='company_registered'),
    path('products/create', CreateProducts.as_view(), name='create-products'),
    path('products', ProductsList.as_view(), name='product-list'),
    path('products/edit/<pk>', ProductEdit.as_view(), name='product-edit'),
    path('products/delete/<pk>', ProductDelete.as_view(), name='product-delete'),
    path('change-user-status/<pk>', change_stock_status, name='change-stock-status')
]

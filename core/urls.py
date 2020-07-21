from django.urls import include, path
from .views import RegistryCompany, CompanyRegistered, CreateProducts, ProductsList, ProductEdit, ProductDelete, \
    change_stock_status, OrderList, ajax_order_list

urlpatterns = [
    path('', include('django.contrib.auth.urls'), name="login"),
    path('oauth/', include('social_django.urls', namespace='social')),
    path('company/', RegistryCompany.as_view(), name='company'),
    path('company_registered/<pk>', CompanyRegistered.as_view(), name='company_registered'),
    path('products/create', CreateProducts.as_view(), name='create-products'),
    path('products', ProductsList.as_view(), name='product-list'),
    path('products/edit/<pk>', ProductEdit.as_view(), name='product-edit'),
    path('products/delete/<pk>', ProductDelete.as_view(), name='product-delete'),
    path('change-user-status/<pk>', change_stock_status, name='change-stock-status'),
    path('order', OrderList.as_view(), name='orders'),
    path('order_ajax', ajax_order_list, name='orders-ajax'),
]

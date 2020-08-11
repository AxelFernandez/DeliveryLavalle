from django.urls import include, path
from .views import RegistryCompany, CompanyRegistered, CreateProducts, ProductsList, ProductEdit, ProductDelete, \
    change_stock_status, OrderList, ajax_order_list, get_next_state, ConfigurationCompany, ConfigurationUpdate, \
    update_available_company, Sales, cancel_order, OrderDetail, SendMeliLink

urlpatterns = [
    path('', include('django.contrib.auth.urls'), name="login"),
    path('oauth/', include('social_django.urls', namespace='social')),

    # Company
    path('company/', RegistryCompany.as_view(), name='company'),
    path('company_registered/<pk>', CompanyRegistered.as_view(), name='company_registered'),
    path('configuration', ConfigurationCompany.as_view(), name='configuration'),
    path('configuration_update/<pk>', ConfigurationUpdate.as_view(), name='configuration-update'),
    path('configuration_update_available/<pk>/<redirect>', update_available_company, name='update-available-company'),

    # Products
    path('products/create', CreateProducts.as_view(), name='create-products'),
    path('products', ProductsList.as_view(), name='product-list'),
    path('products/edit/<pk>', ProductEdit.as_view(), name='product-edit'),
    path('products/delete/<pk>', ProductDelete.as_view(), name='product-delete'),

    # User
    path('change-user-status/<pk>', change_stock_status, name='change-stock-status'),

    # Orders
    path('order', OrderList.as_view(), name='orders'),
    path('order_detail/<pk>', OrderDetail.as_view(), name='order-detail'),
    path('order_ajax', ajax_order_list, name='orders-ajax'),
    path('cancel-order/<pk>', cancel_order, name='cancel-order'),
    path('next_state/<pk>', get_next_state, name='next-state'),

    # Sales
    path('sales', Sales.as_view(), name='sales'),

    # Mercado Pago Links
    path('send_links_Meli/<pk>', SendMeliLink.as_view(), name='send-link-meli'),

]

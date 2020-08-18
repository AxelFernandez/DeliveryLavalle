from django.urls import include, path

from core.views.Companyviews import RegistryCompany, CompanyRegistered, ConfigurationCompany, ConfigurationUpdate, \
    update_available_company
from core.views.MeliViews import SendMeliLink, UpdateMeliLink
from core.views.OrdersViews import OrderList, OrderDetail, ajax_order_list, cancel_order, get_next_state
from core.views.ProductsViews import CreateProducts, ProductsList, ProductEdit, ProductDelete
from core.views.SalesViews import Sales, process_paid_cron_start, PeriodsPaymentServices, SalesInMonth, pay_service
from core.views.UserViews import change_stock_status

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
    path('process_all_paid', process_paid_cron_start),
    path('periods/', PeriodsPaymentServices.as_view(), name='periods'),
    path('periods_detail/<pk>', SalesInMonth.as_view(), name='periods-detail'),


    # Mercado Pago Links
    path('send_link_Meli/<pk>', SendMeliLink.as_view(), name='send-meli-link'),
    path('update_link_meli/<pk>', UpdateMeliLink.as_view(), name='update-meli-link'),



]

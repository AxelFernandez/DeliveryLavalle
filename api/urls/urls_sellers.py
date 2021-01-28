from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from api.views.customer_api import FirebaseTokenApi, CompanyCategories, Review, MeliLinkApi
from api.views.seller_api import GoogleViewSeller, CreateCompany, GetOrdersPending, GetOrdersInProgress, \
    GetOrdersClosed, GetOrdersById, SetOrdersInNewState, CancelOrder, ProductsCategory, ProductCategoryDelete, Product, \
    ProductDelete, AccountDebit, MeliLinkSeller, InvoiceApi, InvoicePendingApi, CompanyAvailability

urlpatterns = [
    path('google', GoogleViewSeller.as_view(), name='google'),
    path('firebase_token', FirebaseTokenApi.as_view(), name='firebase-token'),

    path('company_category', CompanyCategories.as_view(), name='comapny-category-api'),
    path('company', CreateCompany.as_view(), name='create-company'),
    path('order_pending', GetOrdersPending.as_view(), name='get-order-pending'),
    path('order_closed', GetOrdersClosed.as_view(), name='get-order-closed'),
    path('order_in_progress', GetOrdersInProgress.as_view(), name='get-order-in-progress'),
    path('order_by_id', GetOrdersById.as_view(), name='get-order-by-id'),
    path('next_state', SetOrdersInNewState.as_view(), name='next-state-api'),
    path('cancel', CancelOrder.as_view(), name='cancel-order'),
    path('product_category', ProductsCategory.as_view(), name='product-category'),
    path('product_category_delete', ProductCategoryDelete.as_view(), name='product-category-delete'),
    path('product', Product.as_view(), name='product'),
    path('product_delete', ProductDelete.as_view(), name='product-delete'),
    path('account_debit', AccountDebit.as_view(), name='account-debit'),
    path('reviews', Review.as_view(), name='view-reviews'),
    path('sendMeliLink', MeliLinkSeller.as_view(), name='meli-link-seller'),
    path('getMeliLink', MeliLinkApi.as_view(), name='meli-link-customer'),
    path('invoices', InvoiceApi.as_view(), name='invoices'),
    path('hadPendingInvoices', InvoicePendingApi.as_view(), name='invoices-pending'),
    path('company_availability', CompanyAvailability.as_view(), name='company-availability'),

]
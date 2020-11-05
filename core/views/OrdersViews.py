import requests
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView, DetailView

import core
from core.models import Company, Order, DetailOrder, MeliLinks, Products, State, FirebaseToken
from core.views.Companyviews import get_company
from core.views.SalesViews import apply_usage
from utils.env import get_env_variable


def ajax_order_list(request):
    company_id = Company.objects.get(id_user=request.user)
    return HttpResponse((Order.objects.filter(id_company=company_id).count()))


class OrderList(LoginRequiredMixin, ListView):
    template_name = 'core/order_list.html'
    model = Order
    paginate_by = 3
    len_orders = None

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(OrderList, self).get_context_data()
        context['orders_len'] = self.len_orders
        context['ajax_active'] = settings.AJAX_ACTIVE
        for order in context['object_list']:
            order.products = []
            order.next_state = get_next_state_str(order)
            query_order_products = DetailOrder.objects.filter(order_id=order.id)
            order.is_MP = False
            if order.payment_method.description == 'Mercado Pago':
                order.is_MP = True
                if len(MeliLinks.objects.filter(order=order)) == 0:
                    order.is_MeliLink_sent = False
                else:
                    order.is_MeliLink_sent = True
            for ids in query_order_products:
                product = Products.objects.get(pk=ids.product_id)
                order.products.append(
                    {'quantity': ids.quantity, 'name': product.name, 'description': product.description, 'price': product.price})
        return context

    def get_queryset(self):
        company_id = Company.objects.get(id_user=self.request.user)
        query_set = Order.objects.filter(id_company=company_id).exclude(state=5).exclude(state=6).order_by('-date')
        self.len_orders = len(query_set)
        return query_set


class OrderDetail(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'core/order_detail.html'


def get_next_state(request,pk):
    order = Order.objects.get(pk=pk)
    if order.state.description != core.STATES[5]:  # If the order is not in the last state, add one state
        order_to_search = order.state.id+1
        if order_to_search == 3 and order.retry_in_local:
            order_to_search += 1
        if order_to_search ==4 and not order.retry_in_local:
            order_to_search += 1
        order.state = State.objects.get(pk=order_to_search)
        order.save()
        text_to_notification = get_text_to_notification_client(order_to_search)
        title = "Novedades de "+order.id_company.name
        send_notification_to_customers(order, text_to_notification, title)

    if order.state.description == core.STATES[5]:
        add_debit(request.user,order)
    return HttpResponseRedirect(reverse('orders'))


def get_text_to_notification_client(number):
    if number == 2:
        return "Tu Pedido fue confirmado, y esta siendo preparado"
    if number == 3:
        return "Tu Pedido esta en Camino!"
    if number == 4:
        return "Tu pedido esta listo para retirar por el local del vendedor"
    if number == 5:
        return "Entregamos tu pedido, que lo disfrutes"


def send_notification_to_customers(order, text, title):
    tokens = FirebaseToken.objects.filter(user=order.client.user)
    tokens_array = []
    for token in tokens:
        tokens_array.append(token.token)

    payload = {"Authorization": "key="+get_env_variable('FIREBASE_TOKEN'),
               "Content-Type": "application/json"
               }
    data = {"registration_ids": tokens_array,
            "notification": {
            "title": title,
            "body": text
          }
        }.__str__().replace('\'', '"')
    r = requests.post('https://fcm.googleapis.com/fcm/send', data=data, headers = payload)
    r.text

def get_next_state_str(order):
    pk_to_search = order.state.id + 1
    if pk_to_search == 3 and order.retry_in_local:
        pk_to_search += 1
    if pk_to_search == 4 and not order.retry_in_local:
        pk_to_search += 1
    state = core.STATES[pk_to_search]
    return state


def add_debit(user, order):
    company = get_company(user)
    debit = apply_usage(order.total)
    company.account_debit += debit
    company.save()


def cancel_order(request, pk):
    order = Order.objects.get(pk=pk)
    order.state = State.objects.get(pk=6)
    order.save()
    return HttpResponseRedirect(reverse('orders'))


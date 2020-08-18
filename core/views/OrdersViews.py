from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView, DetailView

import core
from core.models import Company, Order, DetailOrder, MeliLinks, Products, State
from core.views.Companyviews import get_company
from core.views.SalesViews import apply_usage


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
            order.next_state = core.STATES[order.state.id + 1]
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
        query_set = Order.objects.filter(id_company=company_id).exclude(state=4).exclude(state=5).order_by('-date')
        self.len_orders = len(query_set)
        return query_set


class OrderDetail(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'core/order_detail.html'


def get_next_state(request,pk):
    order = Order.objects.get(pk=pk)
    if order.state.description != core.STATES[4]:  # If the order is not in the last state, add one state
        order.state = State.objects.get(pk=order.state.id+1)
        order.save()
    if order.state.description == core.STATES[4]:
        add_debit(request.user,order)
    return HttpResponseRedirect(reverse('orders'))


def add_debit(user, order):
    company = get_company(user)
    debit = apply_usage(order.total)
    company.account_debit += debit
    company.save()


def cancel_order(request, pk):
    order = Order.objects.get(pk=pk)
    order.state = State.objects.get(pk=5)
    order.save()
    return HttpResponseRedirect(reverse('orders'))


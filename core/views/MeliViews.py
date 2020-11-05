from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.datetime_safe import datetime
from django.views.generic import CreateView, UpdateView

from core.form import FormMeliLinks
from core.models import MeliLinks, Order, PaymentService, MeLiTransaction
from core.views.OrdersViews import send_notification_to_customers


class SendMeliLink(LoginRequiredMixin, CreateView):
    model = MeliLinks
    template_name = 'core/meli_link.html'
    form_class = FormMeliLinks

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            self.object = form.save(commit=False)
            self.object.order = Order.objects.get(pk=self.kwargs['pk'])
            title = "Esta disponible tu Link de Pago de " + self.object.order.id_company.name
            body = "Entra a la app y buscalo en mis ordenes"
            send_notification_to_customers(self.object.order, body, title)
            return super().form_valid(form)
        else:
            reverse('login')

    def get_success_url(self):
        return reverse('orders')


class UpdateMeliLink(LoginRequiredMixin, UpdateView):
    model = MeliLinks
    template_name = 'core/meli_link.html'
    form_class = FormMeliLinks

    def get_success_url(self):
        return reverse('orders')


def process_payment(request,*args,**kwargs):
    payment = PaymentService.objects.get(pk=kwargs['pk'])
    response = request.POST
    meli_transaction = MeLiTransaction.objects.create(preference_id=response.get('preference_id'),
                                                      payment_id=response.get('payment_id'),
                                                      payment_status=response.get('payment_status'),
                                                      payment_status_detail=response.get('payment_status_detail'),
                                                      merchant_order_id=response.get('merchant_order_id'),
                                                      processing_mode=response.get('processing_mode'),
                                                      payment_service=payment
                                                      )
    if meli_transaction.payment_status == 'approved':
        payment.payment_status = 'Pagado'
        payment.transaction_date = datetime.now()
        payment.save()
    return HttpResponseRedirect(reverse('periods'))
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.datetime_safe import datetime
from django.views.generic import ListView

from core.models import Order, Company, PaymentService
from core.views.Companyviews import get_company


class Sales(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'core/sales_list.html'
    paginate_by = 10

    def get_queryset(self):
        company_id = get_company(self.request.user)
        query_set = Order.objects.filter(id_company=company_id, state__in=[4, 5]).order_by('-date')
        return query_set

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(Sales, self).get_context_data()
        company = get_company(self.request.user)
        payment_pending = PaymentService.objects.filter(company=company,payment_status='Pendiente').count()
        context['have_debt'] = False
        if payment_pending != 0:
            context['have_debt'] = True
        return context


# This must run once per mouth
def process_paid_cron_start(request):
    all_company = Company.objects.all()
    period = '{}/{}'.format(datetime.now().month,datetime.now().year)
    for company in all_company:
        if company.account_debit != 0.0:
            PaymentService.objects.create(company=company,
                                          payment_status='Pendiente',
                                          mount=company.account_debit,
                                          transaction_date=None,
                                          period=period
                                          )
            company.account_debit = 0.0
            company.save()
    return HttpResponseRedirect(reverse('orders'))


class PeriodsPaymentServices(LoginRequiredMixin,ListView):
    model = PaymentService
    template_name = 'core/periods_payment_service.html'
    paginate_by = 10

    def get_queryset(self):
        return PaymentService.objects.filter(company=get_company(self.request.user)).order_by('-payment_date')


class SalesInMonth(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'core/period_detail.html'

    def get_queryset(self,*args,**kwargs):
        period = PaymentService.objects.get(pk=self.kwargs['pk']).period.split('/')
        return Order.objects.filter(date__month=period[0],
                                    date__year=period[1])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(SalesInMonth, self).get_context_data()
        total = 0
        usage = 0
        for order in self.object_list:
            total += order.total
            # TODO: Separate the usage formula in a separate function
            order.usage = round(order.total * 0.04, 2)
            usage += order.usage
        context['total'] = total
        context['usage'] = round(usage, 2)

        # TODO: Check if this is not necessary in the future, this is only for security
        payment_mount = PaymentService.objects.get(pk=self.kwargs['pk']).mount
        context['warning'] = False
        if payment_mount != context['usage']:
            context['warning'] = True
        return context



from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from django.template.defaultfilters import register

from core.form import FormCompany
from core.models import Company


class RegistryCompany(LoginRequiredMixin, CreateView):
    template_name = 'core/create_company.html'
    model = Company
    success_url = reverse_lazy('company_registered')
    form_class = FormCompany

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

    def render_to_response(self, context, **response_kwargs):
        had_company = Company.objects.filter(id_user=self.request.user.id).first()
        if had_company is not None:
            return HttpResponseRedirect(reverse("orders"))
        return super(RegistryCompany, self).render_to_response(context, **response_kwargs)

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            self.object = form.save(commit=False)
            self.object.id_user = self.request.user
            self.object.account_debit = 0.0
            return super().form_valid(form)
        else:
            reverse('login')

    def get_success_url(self):
        return reverse('company_registered', args=(self.object.id,))


class CompanyRegistered(LoginRequiredMixin, DetailView):
    template_name = 'core/company_registered.html'
    model = Company


class ConfigurationCompany(LoginRequiredMixin,ListView):
    model = Company
    template_name = 'core/configuration_list.html'

    def get_queryset(self):
        return Company.objects.filter(id_user=self.request.user.id)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ConfigurationCompany, self).get_context_data()
        company = context['object_list'].first()
        payment_method = []
        for method in company.payment_method.all():
            payment_method.append(method)
        context['payment_method'] = payment_method
        return context


class ConfigurationUpdate(LoginRequiredMixin, UpdateView):
    model = Company
    template_name = 'core/create_company.html'
    success_url = reverse_lazy('product-list')
    form_class = FormCompany



def update_available_company(request, pk, redirect = None):
    company = Company.objects.get(pk=pk)
    if company.available_now == "SI":
        company.available_now = 'NO'
        company.save()
    else:
        company.available_now = 'SI'
        company.save()
    return HttpResponseRedirect(reverse(redirect))


# TODO: Refactor this in all Company.objects.get
@register.simple_tag()
def get_company(user):
    return Company.objects.get(id_user=user)


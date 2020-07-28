from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView, TemplateView

import core
from core.form import FormCompany, FormProducts
from core.models import Company, Products as Prod, Products, Order, DetailOrder, State


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
        return super(RegistryCompany, self).render_to_response(context,**response_kwargs)
        
    def form_valid(self, form):
        if self.request.user.is_authenticated:
            self.object = form.save(commit=False)
            self.object.id_user = self.request.user
            return super().form_valid(form)
        else:
            reverse('login')

    def get_success_url(self):
        return reverse('company_registered', args=(self.object.id,))


class CompanyRegistered(LoginRequiredMixin, DetailView):
    template_name = 'core/company_registered.html'
    model = Company


class CreateProducts(LoginRequiredMixin, CreateView):
    template_name = 'core/create_products.html'
    model = Products
    form_class = FormProducts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            self.object = form.save(commit=False)
            self.object.id_company = Company.objects.get(id_user=self.request.user)
            return super().form_valid(form)
        else:
            reverse('login')

    def get_success_url(self):
        return reverse('product-list')  # args=(self.object.id_company,))


class ProductsList(LoginRequiredMixin, ListView):
    model = Products
    template_name = 'core/products_list.html'

    def get_queryset(self,**kwargs):
        company_id = Company.objects.get(id_user=self.request.user)
        return Prod.objects.filter(id_company=company_id)


def change_stock_status(request, pk):
    new_status = request.POST.get('active')
    product = get_object_or_404(Prod, id=pk)
    if new_status == 'activate':
        product.is_available= "SI"
    elif new_status == 'deactivate':
        product.is_available = "NO"
    product.save()
    return HttpResponseRedirect(reverse('product-list'))


class ProductEdit(LoginRequiredMixin,UpdateView):
    model = Products
    template_name = 'core/edit_products.html'
    success_url = reverse_lazy('product-list')
    form_class = FormProducts


class ProductDelete(LoginRequiredMixin, DeleteView):
    model = Products
    success_url = reverse_lazy('product-list')
    template_name = 'core/delete_products.html'


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
            for ids in query_order_products:
                product = Products.objects.get(pk=ids.product_id)
                order.products.append(
                    {'quantity': ids.quantity, 'name': product.name, 'description': product.description})
        return context

    def get_queryset(self):
        company_id = Company.objects.get(id_user=self.request.user)
        query_set = Order.objects.filter(id_company=company_id).exclude(state=4).order_by('-date')
        self.len_orders = len(query_set)
        return query_set


def get_next_state(request,pk):
    order = Order.objects.get(pk=pk)
    if order.state.id != core.STATES[4]:  # If the order is not in the last state, add one state
        order.state = State.objects.get(pk=order.state.id+1)
        order.save()
    return HttpResponseRedirect(reverse('orders'))


def update_available_company(request,pk):
    company = Company.objects.get(pk=pk)
    if company.available_now == "SI":
        company.available_now = 'NO'
        company.save()
    else:
        company.available_now = 'SI'
        company.save()
    return HttpResponseRedirect(reverse('configuration'))


class ConfigurationCompany(LoginRequiredMixin,ListView):
    model = Company
    template_name = 'core/configuration_list.html'

    def get_queryset(self):
        return Company.objects.filter(id_user=self.request.user.id)


class ConfigurationUpdate(LoginRequiredMixin, UpdateView):
    model = Company
    template_name = 'core/configuration_update.html'
    success_url = reverse_lazy('product-list')
    form_class = FormProducts

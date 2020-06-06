from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect


from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, ListView

from core.form import FormCompany, FormProducts
from core.models import Company, Products


def register(request):
    if request.method == "POST":

        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'core/create_user.html', {'form': form})


class RegistryCompany(LoginRequiredMixin,CreateView):
    template_name = 'core/create_company.html'
    model = Company
    success_url = reverse_lazy('company_registered')
    form_class = FormCompany

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

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
    success_url = reverse_lazy('products_list')
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
        return reverse('product-list') # args=(self.object.id_company,))


class Products(LoginRequiredMixin, ListView):
    model = Products
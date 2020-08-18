from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView

from core.form import FormProducts
from core.models import Products, Company


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
    paginate_by = 5

    def get_queryset(self,**kwargs):
        company_id = Company.objects.get(id_user=self.request.user)
        return Products.objects.filter(id_company=company_id)


class ProductEdit(LoginRequiredMixin,UpdateView):
    model = Products
    template_name = 'core/edit_products.html'
    success_url = reverse_lazy('product-list')
    form_class = FormProducts


class ProductDelete(LoginRequiredMixin, DeleteView):
    model = Products
    success_url = reverse_lazy('product-list')
    template_name = 'core/delete_products.html'


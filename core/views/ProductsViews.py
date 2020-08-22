from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView

from core.form import FormProducts, FormCategory
from core.models import Products, Company, ProductCategories
from core.views.Companyviews import get_company


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


class CategoryProductCreate(LoginRequiredMixin, CreateView):
    model = ProductCategories
    success_url = reverse_lazy('product-category-list')
    template_name = 'core/create_product_category.html'
    form_class = FormCategory

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.company = get_company(self.request.user)
        return super().form_valid(form)

class CategoryProductUpdate(LoginRequiredMixin, UpdateView):
    model = ProductCategories
    success_url = reverse_lazy('product-category-list')
    template_name = 'core/update_product_category.html'
    form_class = FormCategory



class CategoryProductDelete(LoginRequiredMixin, DeleteView):
    model = ProductCategories
    success_url = reverse_lazy('product-category-list')
    template_name = 'core/delete_product_category.html'
    form_class = FormCategory


class CategoryProductList(LoginRequiredMixin,ListView):
    model = ProductCategories
    template_name = 'core/list_product_category.html'
    form_class = FormCategory

    def get_queryset(self):
        return ProductCategories.objects.filter(company=get_company(self.request.user))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoryProductList, self).get_context_data()
        for category in self.object_list:
            products = Products.objects.filter(category=category).count()
            category.products_in = products
        return context

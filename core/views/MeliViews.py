from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import CreateView, UpdateView

from core.form import FormMeliLinks
from core.models import MeliLinks, Order


class SendMeliLink(LoginRequiredMixin, CreateView):
    model = MeliLinks
    template_name = 'core/meli_link.html'
    form_class = FormMeliLinks

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            self.object = form.save(commit=False)
            self.object.order = Order.objects.get(pk=self.kwargs['pk'])
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

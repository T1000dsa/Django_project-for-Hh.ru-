from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from ads.utils import DataMixin
from django.http import HttpResponse


class IndexHome(DataMixin, TemplateView):
    template_name = 'ads/main_page.html'
    title_page = 'home'

    def get_context_data(self, **kwargs):
        contex = super().get_context_data(**kwargs)
        return self.get_mixin_context(
            contex)
from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from ads.utils import DataMixin
from django.http import HttpResponse

def page_not_found(request, exception):
    return render(request, 'ads/not_found.html')
    

class IndexHome(DataMixin, TemplateView):
    template_name = 'ads/main_page.html'
    title_page = 'Главная'

    def get_context_data(self, **kwargs):
        contex = super().get_context_data(**kwargs)
        return self.get_mixin_context(
            contex)
    
    
class CreateTender(DataMixin, TemplateView):
    template_name = 'ads/create_tender.html'
    title_page = 'Добавить Объявление'

    def get_context_data(self, **kwargs):
        contex = super().get_context_data(**kwargs)
        return self.get_mixin_context(
            contex)
       
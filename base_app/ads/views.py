from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, DetailView, FormView, CreateView, UpdateView, DeleteView, ListView
from ads.utils import DataMixin
from django.http import HttpResponse
from ads.models import Ad, ExchangeProposal
from ads.forms import AdForm, ExchangeProposalForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth import get_user_model
from django.http import HttpRequest, Http404
from django.core.exceptions import PermissionDenied
import logging

logger = logging.getLogger(__name__)



def page_not_found(request, exception):
    return render(request, 'ads/not_found.html')
    

class IndexHome(DataMixin, TemplateView):
    template_name = 'ads/main_page.html'
    title_page = 'Главная'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(
            context)
    
    
class CreateAd(DataMixin, LoginRequiredMixin, CreateView):
    template_name = 'ads/create_ad.html'
    title_page = 'Добавить Объявление'
    success_url = reverse_lazy('home_page')
    model = Ad
    form_class = AdForm
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
class EditAd(DataMixin, LoginRequiredMixin, UpdateView):
    template_name = 'ads/edit_ad.html'
    title_page = 'Редактировать Объявление'
    fields = '__all__'
    success_url = reverse_lazy('home_page')
    title_page = 'Редактирование Объявления'
    model = Ad

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(
            context)
    
    def get_queryset(self):
        return Ad.objects.filter(user=self.request.user)
    
class DeleteAd(DataMixin, LoginRequiredMixin, DeleteView):
    template_name = 'ads/delete_ad.html'
    title_page = 'Удалить Объявление'
    success_url = reverse_lazy('home_page')
    model = Ad

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(
            context)
    def get_queryset(self):
        return Ad.objects.filter(user=self.request.user)
    
class ShowAds(DataMixin, LoginRequiredMixin, ListView):
    template_name = 'ads/show_ads.html'
    title_page = 'Смотреть Объявления'
    model = Ad

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(
            context,
            index_list=context['ad_list']
            )
    

class ShowAd(DataMixin,LoginRequiredMixin, DetailView):
    template_name = 'ads/show_ad.html'
    title_page = 'Смотреть Объявление'
    model = Ad

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user_pk = self.request if self.request.user.is_authenticated else None
        
        return self.get_mixin_context(
            context,
            current_user=user_pk
        )
    
class CreateExchange(DataMixin, LoginRequiredMixin, CreateView):
    model = ExchangeProposal
    form_class = ExchangeProposalForm
    template_name = 'ads/barter.html'
    success_url = reverse_lazy('offers_list')
    title_page = 'Обмен'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ad_receiver'] = Ad.objects.get(pk=self.kwargs['ad_receiver_id'])
        return context

    def form_valid(self, form):
        try:
            ad_sender = get_object_or_404(
            Ad, 
            user__pk=self.kwargs['ad_sender_id'],
            pk=self.request.user.pk
        )
            ad_receiver = get_object_or_404(Ad, pk=self.kwargs['ad_receiver_id'])


            logger.debug(f'{ad_sender}, {ad_receiver} {self.request.user.pk}')
            
            if ad_sender != self.request.user.pk:
                raise PermissionDenied("Вы не владелец объявления-отправителя!")
            
            if ad_sender == ad_receiver:
                form.add_error(None, "Нельзя предложить обмен на своё же объявление")
                return self.form_invalid(form)
            
            form.instance.ad_sender = ad_sender
            form.instance.ad_receiver = ad_receiver
            form.instance.status = 'pending'
            
            return super().form_valid(form)
            
        except Ad.DoesNotExist:
            raise Http404("Одно из объявлений не найдено")